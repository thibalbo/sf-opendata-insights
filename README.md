# Project Title

SF Open Data Insights

## Getting Started

These instructions will get you a copy of the project up and running on your machine. In order to have the application up and running you will either have to deploy it entirely to your remote machine or part on your remote machine and part on your local machine.

### Prerequisites

You will need to install the shiny server on your remote machine. If you are running ubuntu:

```
sudo apt-get update
sudo apt-get install r-base
sudo apt-get install r-base-dev
sudo su - -c "R -e \"install.packages('shiny', repos = 'http://cran.rstudio.com/')\""
sudo apt-get install gdebi-core
wget https://download3.rstudio.org/ubuntu-12.04/x86_64/shiny-server-1.5.0.831-amd64.deb
sudo gdebi shiny-server-1.5.0.831-amd64.deb
```

We will also use a local database to store our datasets. On your local machine:

```
initdb -D db
pg_ctl -D db -l logfile start
createdb sf_opendata_insights
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used

## Contributing

The best way is to send a pull request.

## Versioning


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
