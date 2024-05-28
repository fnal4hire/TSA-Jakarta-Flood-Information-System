from flask import Flask, render_template, request
import schedule
import time
import threading
import os
import pandas as pd
import matplotlib.pyplot as plt
from scrapper import scrape_floodgate_data  # Sesuaikan nama file jika berbeda

app= Flask(__name__)
#default floodgate_value
pintu_air="Bendung Katulampa"
@app.route('/')
def index():
    global pintu_air
    if request.method=='POST':
        pintu_air=request.form['pintu_air']
    #graph
    graph=create_graph(pintu_air)
    #table
    dict_list=scrape_floodgate_data()
    return render_template('index.html',table=dict_list, plot_path=graph)

def scrape_and_update():
    global pintu_air
    create_graph(pintu_air)
    scrape_floodgate_data()

def scheduler():
    schedule.every().hour.do(scrape_and_update)
    while True:
        schedule.run_pending()
        time.sleep(1)

def create_graph(pintu_air):
    #search for file
    file= "./csv/" + pintu_air.replace(' ','_') + ".csv"
    #if exist do
    if os.path.exists(file):
        #read file
        df=pd.read_csv(file)
        times=df["Time"]
        levels=df["Water Level (cm)"].astype(int)
        #plotting
        plt.figure(figsize=(10,5))
        plt.plot(times, levels, marker='o')
        plt.suptitle(f"{pintu_air}", fontsize=18)
        plt.grid(True)

        #save plot
        dir='.\graph'
        os.makedirs(dir, exist_ok=True)
        gpath=os.path.join(dir,f"{pintu_air.replace(' ','_')}.png")
        plt.savefig(gpath, format='png')
        plt.close()
        return gpath
    return None
if __name__=='__main__':
    scheduler_thread = threading.Thread(target=scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Run the Flask app
    app.run(debug=True)
