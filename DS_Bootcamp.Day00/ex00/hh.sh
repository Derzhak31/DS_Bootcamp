#!/bin/bash

URL='https://api.hh.ru/vacancies?text=data+scientist&per_page=20'
curl $URL | jq . > hh.json