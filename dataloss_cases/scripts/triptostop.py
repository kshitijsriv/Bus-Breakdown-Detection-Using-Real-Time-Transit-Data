import pandas as pd
import pickle


g = pd.read_csv('stops.csv')
st = {}
for j in range(len(g)):
    st[g['stop_id'][j]] = (g['stop_lat'][j], g['stop_lon'][j])

s = pd.read_csv('st.csv')
t = {}
for i in range(len(s)):
    if s['stop_sequence'][i+1] == 0:
        t[s['trip_id'][i]] = st[s['stop_id'][i]]


f = open('trip_to_stop.pkl', 'wb')
pickle.dump(t, f)
f.close()

# fil = open('trip_to_stop.pkl','rb')         #loading all destination coordinates from file wrt the tripid
# tripstop = pickle.load(fil)
# fil.close()

# print(tripstop[3341])
