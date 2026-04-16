import gradio as gr
import matplotlib.pyplot as plt
import folium

def get_weather(day):
    return {
        "Mon":"Clear","Tue":"Cloudy","Wed":"Clear",
        "Thu":"Storm","Fri":"Rain","Sat":"Clear","Sun":"Clear"
    }[day]

locations = [
"Noida Sector 18 Metro","DLF Mall of India","Rajiv Chowk",
"Saket Select City Walk","Huda City Centre","Vaishali Metro",
"Akshardham","India Gate","Karol Bagh","Lajpat Nagar",
"Nehru Place","Rohini Sector 18","Dwarka Sector 21",
"Cyber Hub Gurgaon","MG Road Gurgaon"
]

def traffic_pattern():
    hours = list(range(6,23))
    pattern = []
    for h in hours:
        if h in range(8,10) or h in range(17,20):
            pattern.append(2)
        elif h in range(11,16):
            pattern.append(1)
        else:
            pattern.append(0)
    return hours, pattern

def best_peak():
    hours, pattern = traffic_pattern()
    best_list = [f"{h} to {h+1}" for h,v in zip(hours,pattern) if v==0][:3]
    peak_list = [f"{h} to {h+1}" for h,v in zip(hours,pattern) if v==2][:3]
    return ", ".join(best_list), ", ".join(peak_list)

def crowd(day):
    if day in ["Sat","Sun"]:
        return "🔴 Heavy Crowd (Due to Holiday)"
    return "🟠 Moderate Crowd"

def generate_graph():
    hours, pattern = traffic_pattern()
    fig = plt.figure(figsize=(8,3))
    plt.plot(hours, pattern, marker='o')
    plt.xlabel("Time")
    plt.ylabel("Traffic Level")
    plt.title("Traffic Flow (Best vs Peak)")
    return fig

def generate_map(place):
    coords = {
        "Noida Sector 18 Metro":[28.57,77.32],
        "DLF Mall of India":[28.56,77.32],
        "Rajiv Chowk":[28.63,77.22],
        "Saket Select City Walk":[28.52,77.21],
        "Huda City Centre":[28.46,77.07],
        "Vaishali Metro":[28.64,77.34],
        "Akshardham":[28.61,77.28],
        "India Gate":[28.61,77.23],
        "Karol Bagh":[28.65,77.19],
        "Lajpat Nagar":[28.57,77.24],
        "Nehru Place":[28.55,77.25],
        "Rohini Sector 18":[28.73,77.12],
        "Dwarka Sector 21":[28.55,77.06],
        "Cyber Hub Gurgaon":[28.49,77.08],
        "MG Road Gurgaon":[28.48,77.09]
    }

    lat, lon = coords.get(place,[28.60,77.30])
    m = folium.Map(location=[lat, lon], zoom_start=14)
    folium.Marker([lat, lon], tooltip=place).add_to(m)
    return m._repr_html_()

def predict(day, place):
    weather = get_weather(day)

    if weather == "Rain":
        return ("🌧 Rainy","","","🚫 No Crowd",None,generate_map(place))

    if weather == "Storm":
        return ("⛈ Storm","","","⚠ No Movement",None,generate_map(place))

    best, peak = best_peak()

    return (
        f"🌦 {weather}",
        f"🟢 Best Time: {best}",
        f"🔴 Peak Time: {peak}",
        crowd(day),
        generate_graph(),
        generate_map(place)
    )

with gr.Blocks() as demo:
    gr.Markdown("# 🚦 TraffiX AI")
    day = gr.Dropdown(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
    place = gr.Dropdown(locations)
    btn = gr.Button("Analyze")

    weather = gr.Textbox()
    best = gr.Textbox()
    peak = gr.Textbox()
    crowd_box = gr.Textbox()

    graph = gr.Plot()
    map_box = gr.HTML()

    btn.click(predict,[day,place],[weather,best,peak,crowd_box,graph,map_box])

demo.launch()
