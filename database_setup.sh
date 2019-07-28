#!/usr/bin/env bash

sudo -u postgres psql
CREATE DATABASE haut;
CREATE USER lbhautpguser WITH ENCRYPTED PASSWORD 'u!6[l;$K;q$$ST&U';
GRANT ALL PRIVILEGES ON DATABASE haut TO lbhautpguser;
ALTER DATABASE haut OWNER TO lbhautpguser;