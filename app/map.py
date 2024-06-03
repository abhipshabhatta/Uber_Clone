from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from hashlib import sha256
import config
import certifi
import uuid
import os
import folium
from folium.plugins import MarkerCluster
import geopy
from geopy.geocoders import Nominatim

# this is the latitude and longitude for Paris
start_coords = (48.8566, 2.3522)
# map at the starting location
map_france = folium.Map(location=start_coords, zoom_start=6)
# it add a marker for the starting location in France
folium.Marker(start_coords, popup="Start Location: Paris").add_to(map_france)
# Latitude and Longitude for Lyon
destination_coords = (45.7640, 4.8357)
# it add a marker for the destination in France
folium.Marker(destination_coords, popup="Destination: Lyon").add_to(map_france)
# it save the map to an HTML file
map_france.save("France_map.html")
