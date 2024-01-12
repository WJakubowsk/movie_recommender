#!/bin/bash
#SBATCH --account=ganzha_23
#SBATCH --partition=long,short
#SBATCH --cpus-per-gpu=4
#SBATCH --gpus=a100:2
#SBATCH --time=12:00:00
#SBATCH --mem=150G
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wiktor.jakubowski.stud@pw.edu.pl
#SBATCH --job-name=recommender
#SBATCH --output=/home2/faculty/wjakubowski/logs/recommender/20240112_recommender_10_epochs.log

. /home2/faculty/wjakubowski/miniconda3/etc/profile.d/conda.sh
conda activate mymovies

python /home2/faculty/wjakubowski/MovieRecommender/model/main.py