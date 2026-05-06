# Employee Directory App

A full-stack web application hosted on AWS using a multi-tier VPC architecture.
A Flask app running on EC2 serves employee data from a MySQL database on RDS —
the database sits in a private subnet with no direct internet access.

## Architecture

upload image here

## Services Used

- VPC — custom network with public and private subnets across 2 AZs
- Internet Gateway — connects the VPC to the internet
- Route Tables — public subnets route to IGW, private subnets stay internal
- Security Groups — layered firewall rules between each tier
- Application Load Balancer — receives traffic and forwards to EC2
- EC2 — Flask web server running in public subnet
- RDS MySQL — database running in private subnet, unreachable from internet
- IAM — EC2 instance role

## Live Demo

http://employee-directory-alb-516614506.eu-central-1.elb.amazonaws.com

## Network Architecture

## Security Groups

Internet → lb-sg (port 80)
lb-sg → ec2-sg (port 80, LB only)
ec2-sg → rds-sg (port 3306, EC2 only)
Your IP → bastion-sg (port 22)

Each layer only accepts traffic from the layer directly above it.
The database is completely unreachable from the internet.

## Features

- View all employees in a dark-themed table
- Add new employees via a form
- Data persists in MySQL on RDS
- App runs as a systemd service — survives SSH disconnects and reboots
- Load Balancer health checks ensure traffic only goes to healthy instances

## How It Works

1. User hits the Load Balancer DNS over HTTP
2. ALB forwards request to EC2 target group
3. Flask app on EC2 queries RDS MySQL in the private subnet
4. Employee data is returned and rendered as HTML

## Setup

1. Create VPC with 4 subnets across 2 AZs
2. Attach Internet Gateway, configure route tables
3. Create 4 security groups with layered rules
4. Launch RDS MySQL in private subnet
5. Launch EC2 in public subnet, install Flask and pymysql
6. Connect EC2 to RDS, run schema.sql to create table
7. Create ALB targeting the EC2 instance
8. Configure Flask app as a systemd service

## What I Learned

- How to build a VPC from scratch with public and private subnets
- How CIDR blocks work and how subnets carve up the VPC range
- Why Multi-AZ matters — one AZ failure doesn't take down the app
- How security groups chain by reference instead of IP address
- How a Load Balancer health check works and what unhealthy means
- How to SSH into EC2 and configure a Linux server manually
- How to run a Python app as a persistent systemd service
- The difference between public and private subnets at the network level

## Challenges

- Flask app didn't start from user data script on first boot — had to SSH
  in and install dependencies manually
- pymysql not installed by default on Amazon Linux 2023 — mysql package
  also renamed to mariadb105
- App stopped when SSH session closed — fixed by creating a systemd service
  that restarts automatically on failure or reboot
- heredoc syntax didn't work cleanly in PowerShell SSH session — used
  nano to edit files directly on the instance instead

## Author

Made by Ahmed Mohammed Baz
