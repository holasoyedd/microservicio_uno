from django.shortcuts import render
from django.http import (Http404, HttpResponse, HttpResponseNotAllowed,
                        HttpResponseNotFound, HttpResponseRedirect,
                        HttpResponseServerError, JsonResponse, request)
from django.views.decorators.csrf import csrf_exempt
import requests
import json

@csrf_exempt
def searchComics(request):
    if not request.method == 'POST':
        return HttpResponseNotAllowed('')
    else:
        my_json = request.body.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        listaRespuesta = []
        respuesta = ""

        #si busca por comic
        if data["palabraBusqueda"] != "" and data["buscarPor"] == "C":
            respuesta = requests.get("https://gateway.marvel.com:443/v1/public/comics?titleStartsWith="+data["palabraBusqueda"]+"&apikey=2b1be57a5bd361fead51e503552814df&hash=ed44855d7f782ef59c74218340784ffd&ts=1")
            respuestaJson = respuesta.json()

            respuestaLista = respuestaJson["data"].get("results")
            
            for elemento in respuestaLista:
                llavesAObtener = ["id", "title"]
                a_subset = {key: elemento[key] for key in llavesAObtener}

                urlImage = elemento["thumbnail"]["path"]+"."+elemento["thumbnail"]["extension"]

                onSaleDate = elemento["dates"][0]["date"]

                a_subset["image"] = urlImage
                a_subset["onsaleDate"] = onSaleDate

                listaRespuesta.append(a_subset)
                return HttpResponse(json.dumps(listaRespuesta), content_type="application/json")

        #si busca por personaje
        elif data["palabraBusqueda"] != "" and data["buscarPor"] == "P":
            respuesta = requests.get("https://gateway.marvel.com:443/v1/public/characters?nameStartsWith="+data["palabraBusqueda"]+"&apikey=2b1be57a5bd361fead51e503552814df&hash=ed44855d7f782ef59c74218340784ffd&ts=1")
        #si no ingresa el nombre
        else:
            respuesta = requests.get("https://gateway.marvel.com:443/v1/public/characters?apikey=2b1be57a5bd361fead51e503552814df&hash=ed44855d7f782ef59c74218340784ffd&ts=1")

        respuestaJson = respuesta.json()
        respuestaLista = respuestaJson["data"].get("results")
            
        for elemento in respuestaLista:
            llavesAObtener = ["id", "name"]
            a_subset = {key: elemento[key] for key in llavesAObtener}
                
            urlImage = elemento["thumbnail"]["path"]+"."+elemento["thumbnail"]["extension"]
            apariciones = elemento["comics"]["available"]

            a_subset["image"] = urlImage
            a_subset["appearances"] = apariciones

            listaRespuesta.append(a_subset)
        return HttpResponse(json.dumps(listaRespuesta), content_type="application/json")
        #return HttpResponse("nice", content_type="application/json")