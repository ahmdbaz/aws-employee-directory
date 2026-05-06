# Employee Directory App

A full-stack web application hosted on AWS using a multi-tier VPC architecture.
A Flask app running on EC2 serves employee data from a MySQL database on RDS —
the database sits in a private subnet with no direct internet access.

## Architecture

<img width="1024" height="1536" alt="6b69d078-b309-43fa-973f-9f37d70e0481" src="https://github.com/user-attachments/assets/ce70fff3-0412-456c-ba7b-c28ccd4b8f1c" /><img width="1774" height="887" alt="fa518d4c-d374-4bc3-b6b9-332c078f2872" src="https://github.com/user-attachments/assets/ecd2a47b-d122-4146-b2ef-cca97908b720" />


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

## Security Groups

<img width="1024" height="1536" alt="00d02c28-f4ee-4472-9647-6ff2ef6afeff" src="https://github.com/user-attachments/assets/ea1dc9a9-ce47-4b3a-995a-b9a0a6d54aa1" /><img width="1536" height="1024" alt="7004f9a2-9c77-42c1-8f51-4742553d7c34" src="https://github.com/user-attachments/assets/f07b4def-8e8a-4e83-8206-1952c4074dfb" />

Each layer only accepts traffic from the layer directly above it.
The database is completely unreachable from the internet.

## Features

- View all employees in a table
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
