#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:a100:1
#SBATCH --time=24:10:00
#SBATCH --mem=32GB
#SBATCH --job-name=mmgnn
#SBATCH --output=./logs/mmgnn_%j.out

module purge
module load anaconda3/2020.07
eval "$(conda shell.bash hook)"
conda activate hpml-env

cd /scratch/am11533/multimodal-gnn-attn

python main.py --batchsize 16 --epochs 20 --optim Adam