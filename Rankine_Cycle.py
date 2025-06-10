from flask import Flask, render_template, request
import CoolProp.CoolProp as CP

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        try:
            # Get form data
            P2 = float(request.form['P2'])
            T3 = float(request.form['T3'])
            P4 = float(request.form['P4'])
            nT = float(request.form['nT'])
            nP = float(request.form['nP'])
            
            # Calculations
            fluid = 'Water'
            P2 = P2 * 1000
            P3 = P2
            P4 = P4 * 1000
            P1 = P4
            T3 = T3 + 273.15

            s3 = CP.PropsSI('S', 'T', T3, 'P', P3, fluid)
            h3 = CP.PropsSI('H', 'T', T3, 'P', P3, fluid)
            s4s = s3
            h4s = CP.PropsSI('H', 'S', s4s, 'P', P4, fluid)
            h4a = h3 - (nT * (h3-h4s))
            x4 = CP.PropsSI('Q','P',P4,'H',h4a,fluid)

            h1 = CP.PropsSI('H','Q',0,'P',P1,fluid)
            T1 = CP.PropsSI('T','Q',0,'P',P1,fluid)
            s1 = CP.PropsSI('S','Q',0,'P',P1,fluid)
            s2s = s1
            h2s = CP.PropsSI('H','S',s2s,'P',P2,fluid)
            h2a = ((1/nP)*(h2s-h1))+h1

            wts = h3-h4s
            wta = h3-h4a
            qout = h4a - h1
            qin = h3 - h2a
            wps = h2s-h1
            wpa = h2a-h1

            s3 = s3/1000
            wts = wts/1000
            wta = wta/1000
            qout = qout/1000
            qin = qin/1000
            wps = wps/1000
            wpa = wpa/1000

            wnet = wta - wpa
            teff = wnet/qin

            results = {
                'wta': f"{wta:.2f}",
                'wpa': f"{wpa:.2f}",
                'wnet': f"{wnet:.2f}",
                'x4': f"{x4:.3f}",
                'qout': f"{qout:.2f}",
                'qin': f"{qin:.2f}",
                'teff': f"{teff:.2f}"
            }
        except Exception as e:
            results = {'error': str(e)}

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)