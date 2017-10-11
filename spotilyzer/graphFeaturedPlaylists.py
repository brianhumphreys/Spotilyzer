#!/usr/bin/env python3
######################

import getData as gd
import requests
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
from matplotlib import style
import itertools
import numpy as np

style.use("ggplot")

#20 different colors for graphing
COLORS = itertools.cycle(["#f4c242", "#61a323", "#161efc", "#cc37c7",
			"#ff0000", "#f6ff05", "#000000", "#706c6c",
			"#7200ff", "#4d8e82", "#c1fff3", "#7a89e8",
			"#82689b", "b", "g", "r", "c", "m", "y", "w",])


#The goal of this analysis is to predict which playlist a given song belongs to using KNN
#will use 3 features of the songs, randomly choosing danceability, instrumentalness, speechiness

#add getPlayist(pid)
#add getGenre("Genre")

def createDataFrame(afpd, features):
	preFrameDict = {}
	for i in features:
		preFrameDict[i] = []
	preFrameDict["songid"] = []
	preFrameDict["playlist"] = []
	for i in sorted(afpd.keys()):
		for j in afpd[i]:
			preFrameDict["playlist"].append(i)
			preFrameDict["songid"].append(j["songid"])
			for q in features:
				preFrameDict[q].append(j[q])
	df = pd.DataFrame(preFrameDict)
	#normalize data
	min_max_scaler = preprocessing.MinMaxScaler()
	for i in features:
		df[i] = pd.DataFrame(min_max_scaler.fit_transform(df[i]))
	return df.set_index("songid")

def graph3DAllNodes(df, features):
	if len(features) == 3:
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		xs = df[features[0]]
		ys = df[features[1]]
		zs = df[features[2]]
		ax.scatter(xs, ys, zs, c='g', marker='o')


		ax.set_xlabel(features[0])
		ax.set_ylabel(features[1])
		ax.set_zlabel(features[2])
		plt.show()
	else:
		print("need 3 features to do 3D graph")

def graph2DAllNodes(df, features):
	if len(features) == 2:

		xs = df[features[0]]
		ys = df[features[1]]
		plt.scatter(xs, ys, c='g', marker='o')


		plt.xlabel = features[0]
		plt.ylabel = features[1]
		plt.show()
	else:
		print("need 2 features to do 3D graph")

def graph2DPlaylistsDifferentColors(df, features, playlists):
	if len(features) == 2:
		for i in list(range(0,len(playlists))):
			pdf = df[df["playlist"] == playlists[i]]
			xs = pdf[features[0]]
			ys = pdf[features[1]]
			plt.scatter(xs, ys, color=next(COLORS), marker='o')
		plt.xlabel = features[0]
		plt.ylabel = features[1]
		plt.show()
	else:
		print("need 2 features to do 3D graph")

def graph3DPlaylistsDifferentColors(df, features, playlists):
	if len(features) == 3:
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		for i in list(range(0,len(playlists))):
			pdf = df[df["playlist"] == playlists[i]]
			xs = pdf[features[0]]
			ys = pdf[features[1]]
			zs = pdf[features[2]]
			ax.scatter(xs, ys, zs, c=next(COLORS), marker='o')

		ax.set_xlabel(features[0])
		ax.set_ylabel(features[1])
		ax.set_zlabel(features[2])
		plt.show()
	else:
		print("need 3 features to do 3D graph")

def graph3DPlotlyCategoriesDifferentColors(df, features, categories):
	if len(features) == 3:
		traces = []
		for i in list(range(0,len(categories))):
			pdf = df[df["category"] == categories[i]]
			x = pdf[features[0]]
			y = pdf[features[1]]
			z = pdf[features[2]]
			traces.append(go.Scatter3d(
			    x=x,
			    y=y,
			    z=z,
				name=categories[i],
			    mode='markers',
			    marker=dict(
			        size=12,
			        line=dict(
			            color='rgba(217, 217, 217, 0.14)',
			            width=0.5
			        ),
			        opacity=0.8
			    )
			))
		data = traces
		layout = go.Layout(
		    margin=dict(
		        l=0,
		        r=0,
		        b=0,
		        t=0
		    )
		)
		fig = go.Figure(data=data, layout=layout)
		py.plot(fig)
	else:
		print("need 3 features to do 3D graph")

def graph2DPlotlyCategoriesDifferentColors(df, features, categories):
	if len(features) == 2:
		traces = []
		for i in list(range(0,len(categories))):
			pdf = df[df["category"] == categories[i]]
			x = pdf[features[0]]
			y = pdf[features[1]]
			traces.append(go.Scatter(
			    x=x,
			    y=y,
				name=categories[i],
			    mode='markers',
			    marker=dict(
			        size=12,
			        line=dict(
			            color='rgba(217, 217, 217, 0.14)',
			            width=0.5
			        ),
			        opacity=0.8
			    )
			))
		data = traces
		layout = go.Layout(
		    margin=dict(
		        l=0,
		        r=0,
		        b=0,
		        t=0
		    )
		)
		fig = go.Figure(data=data, layout=layout)
		py.plot(fig)
	else:
		print("need 2 features to do 2D graph")

def PCAOnDataFrame(df, features, components):
	pca = PCA(n_components=components)
	pca.fit(df[features])
	newData = pca.transform(df[features])
	preFrameDict = {}
	preFrameDict["songid"] = []
	preFrameDict["playlist"] = []
	for i in list(range(1,components+1)):
		preFrameDict[str(i)] = []
	for i in list(range(0, len(newData))):
		preFrameDict["songid"].append(df.index.tolist()[i])
		preFrameDict["playlist"].append(df["playlist"][i])
		for j in list(range(0,components)):
			preFrameDict[str(j+1)].append(newData[i][j])
	newDataFrame = pd.DataFrame(preFrameDict)
	#normalize data
	min_max_scaler = preprocessing.MinMaxScaler()
	for i in list(range(1,components+1)):
		newDataFrame[str(i)] = pd.DataFrame(min_max_scaler.fit_transform(newDataFrame[str(i)]))
	return newDataFrame.set_index("songid")

#switch this to genere
access_header = gd.getAccessHeader()

featuredPlaylists = requests.get("https://api.spotify.com/v1/browse/featured-playlists", headers=access_header).json()["playlists"]["items"]
allFeaturedPlaylistData = {}
for i in featuredPlaylists:
	tracks = requests.get(i["href"] + "/tracks", headers=access_header).json()["items"]
	tracksList = []
	for j in tracks:
		tracksList.append(j["track"]["id"])
	allFeaturedPlaylistData[i["id"]] = gd.getSongs(tracksList)

allFeatures = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

playlists = sorted(list(allFeaturedPlaylistData.keys()))
df = createDataFrame(allFeaturedPlaylistData, allFeatures)
#pcadf = PCAOnDataFrame(df, allFeatures, 2)
#graph2DPlaylistsDifferentColors(pcadf, ['1','2'], playlists)
#pcadf = PCAOnDataFrame(df, allFeatures, 3)
#graph3DPlaylistsDifferentColors(pcadf, ['1','2', '3'], playlists)
#graph3DPlaylistsDifferentColors(df, ['popularity','danceability', 'loudness'], playlists)
#graph3DPlaylistsDifferentColors(df, ['acousticness','instrumentalness', 'valence'], playlists)

pcadf = PCAOnDataFrame(df, allFeatures, 2)
graph2DPlaylistsDifferentColors(pcadf, ['1','2'], playlists[0:5])

pcadf = PCAOnDataFrame(df, allFeatures, 3)
graph3DPlaylistsDifferentColors(pcadf, ['1','2', '3'], playlists[0:5])
