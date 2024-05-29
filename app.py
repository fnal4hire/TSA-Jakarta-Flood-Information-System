from flask import Flask, render_template, request, jsonify
import schedule
import time
import threading
import os
import pandas as pd
import matplotlib.pyplot as plt
import urllib.parse
from scrapper import scrape_floodgate_data  # Sesuaikan nama file jika berbeda

app= Flask(__name__)
#default floodgate_value
floodgate=[ "Bendung Katulampa","Pos Depok","PA. Karet","Manggarai BKB","Pasar Ikan - Laut","Pos Angke Hulu","Pos Cipinang Hulu","Pos Krukut Hulu","Pos Pesanggrahan","Pos Sunter Hulu","Pulo Gadung","Waduk Pluit"]
@app.route('/')
def index():
    #graph
    create_graph()
    #table
    dict_list=scrape_floodgate_data()
    return render_template('index.html',table=dict_list)

def scrape_and_update():
    create_graph()
    scrape_floodgate_data()

def scheduler():
    schedule.every().hour.do(scrape_and_update)
    while True:
        schedule.run_pending()
        time.sleep(1)

def create_graph():
    global floodgate
    for item in floodgate:
    #search for file
        file= "./csv/" + item.replace(' ','_') + ".csv"
    #if exist do
        if os.path.exists(file):
        #read file
            df=pd.read_csv(file)
            times=df["Time"]
            levels=df["Water Level (cm)"].astype(int)
        #plotting
            plt.figure(figsize=(10,5))
            plt.plot(times, levels, marker='o')
            plt.suptitle(f"{item}", fontsize=18)
            plt.grid(True)

        #save plot
            dir='.\graph'
            os.makedirs(dir, exist_ok=True)
            gpath=os.path.join(dir,f"{item.replace(' ','_')}.png")
            gpath=urllib.parse.unquote(gpath)
            plt.savefig(gpath, format='png')
            plt.close()
    return None
if __name__=='__main__':
    scheduler_thread = threading.Thread(target=scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Run the Flask app
    app.run(debug=True)
