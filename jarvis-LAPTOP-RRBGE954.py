import pandas as pd
import schedule
import time
from datetime import datetime, timedelta
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ----------------------------
# 1. Setup Offline AI Model
# ----------------------------
model_name = "TheBloke/WizardLM-7B-uncensored-GPTQ"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

def generate_text(prompt, max_length=150):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=max_length)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# ----------------------------
# 2. Local Lead Storage
# ----------------------------
LEAD_FILE = "leads.csv"

# Initialize CSV if not exists
try:
    leads = pd.read_csv(LEAD_FILE)
except FileNotFoundError:
    leads = pd.DataFrame(columns=["Name", "Contact", "Platform", "Status", "FollowUpDate", "Notes"])
    leads.to_csv(LEAD_FILE, index=False)

# ----------------------------
# 3. Add a new lead
# ----------------------------
def add_lead(name, contact, platform):
    follow_up = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    new_lead = pd.DataFrame([[name, contact, platform, "New", follow_up, ""]], 
                            columns=leads.columns)
    new_lead.to_csv(LEAD_FILE, mode='a', header=False, index=False)
    print(f"Lead added: {name} ({platform})")

# ----------------------------
# 4. Follow-up messages
# ----------------------------
def follow_up_leads():
    leads = pd.read_csv(LEAD_FILE)
    today = datetime.now().strftime("%Y-%m-%d")
    
    for i, row in leads.iterrows():
        if row["FollowUpDate"] == today and row["Status"] != "Converted":
            prompt = f"Write a friendly, persuasive follow-up message for {row['Name']} to convert them into a student."
            message = generate_text(prompt)
            print(f"Follow-up message for {row['Name']}:\n{message}\n")
            
            # Schedule next follow-up
            leads.at[i, "FollowUpDate"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    leads.to_csv(LEAD_FILE, index=False)

# ----------------------------
# 5. Ad & content suggestions
# ----------------------------
def ad_idea(prompt):
    full_prompt = f"Suggest a catchy Instagram ad caption + hashtags + short hook for: {prompt}"
    return generate_text(full_prompt)

# ----------------------------
# 6. Schedule tasks
# ----------------------------
schedule.every().day.at("10:00").do(follow_up_leads)

print("Offline AI Jarvis is running...")
while True:
    schedule.run_pending()
    time.sleep(60)

