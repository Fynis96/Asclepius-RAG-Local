#!/bin/bash

set -e

echo "Cleaning up volumes..."
rm -rf /var/lib/postgresql/data/*
rm -rf /data/*
rm -rf /qdrant/storage/*

echo "Volumes have been reset."