import json
import random
from datetime import datetime, timedelta

# Possible values for data generation
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
RELATIVE_DAYS = ["tomorrow", "day after tomorrow", "next Monday", "next Tuesday", "next Wednesday", "next Thursday", "next Friday"]
TIMES = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm"]
TIMEZONES = ["EST", "PST", "CST", "MST", "GMT", "UTC"]
DURATIONS = ["30 minutes", "45 minutes", "1 hour", "90 minutes", "2 hours"]
ATTENDEES = ["John", "Sarah", "the marketing team", "David", "Lisa", "the product team"]

# Sentence templates
TEMPLATES = [
    "Can we meet {date} at {time} {tz} for {duration}?",
    "Let's schedule {duration} meeting {date} around {time}",
    "{attendee} wants to meet {date} {time} {tz}",
    "How about {date} at {time} for {duration}?",
    "I'm free {date} {time} {tz} for {duration}",
    "Do you have time {date} around {time} {tz}?",
    "Meeting request: {date} {time} {tz} with {attendee} for {duration}",
    "Can we do {date} at {time} {tz}? It should take {duration}"
]

def generate_synthetic_data(num_samples=800):
    """Generate synthetic meeting request data"""
    data = []
    
    for i in range(num_samples):
        # Randomly choose template
        template = random.choice(TEMPLATES)
        
        # Randomly choose values
        date = random.choice(RELATIVE_DAYS + DAYS)
        time = random.choice(TIMES)
        tz = random.choice(TIMEZONES)
        duration = random.choice(DURATIONS)
        attendee = random.choice(ATTENDEES)
        
        # Fill template
        text = template.format(
            date=date, time=time, tz=tz, 
            duration=duration, attendee=attendee
        )
        
        # Create annotation (IOB tags - simplified for this example)
        entities = []
        
        # Simple rule-based annotation for demo
        if date in text:
            start_idx = text.find(date)
            entities.append([start_idx, start_idx + len(date), "DATE"])
        if time in text:
            start_idx = text.find(time)
            entities.append([start_idx, start_idx + len(time), "TIME"])
        if tz in text:
            start_idx = text.find(tz)
            entities.append([start_idx, start_idx + len(tz), "TIMEZONE"])
        if duration in text:
            start_idx = text.find(duration)
            entities.append([start_idx, start_idx + len(duration), "DURATION"])
        if attendee in text:
            start_idx = text.find(attendee)
            entities.append([start_idx, start_idx + len(attendee), "ATTENDEE"])
        
        data.append({
            "id": i,
            "text": text,
            "entities": entities
        })
    
    # Split train/test
    train_size = int(0.8 * num_samples)
    train_data = data[:train_size]
    test_data = data[train_size:]
    
    # Save to files
    with open("../data/train_data.json", "w") as f:
        json.dump(train_data, f, indent=2)
    
    with open("../data/test_data.json", "w") as f:
        json.dump(test_data, f, indent=2)
    
    print(f"Generated {len(train_data)} training and {len(test_data)} test samples")
    return data

if __name__ == "__main__":
    generate_synthetic_data(800)