#!/bin/bash

echo "Running ingest"
python ingest/ingest.py

echo "Running app"
exec python app.py  