# SF Open Data Insights

## Intro

Before going straight into the code, let's check out what you'll get. The web app will provide you a lot of different insightful plots. Check a few of them out:

Visualization Networks:
![VisNet](app/static/img/repo/vis.png)

Correlation Plots:
![CorPlot](app/static/img/repo/cor.png)

Time series Plots:
![TSPlot](app/static/img/repo/time.png)

Word clouds:
![WordCloud](app/static/img/repo/word.png)

## Getting Started

These instructions will get you a copy of the project up and running on your machine. In order to have the application up and running you will either have to deploy it entirely to your remote machine or part on your remote machine and part on your local machine.

### Prerequisites

You will need to install the shiny server on your remote machine. If you are running ubuntu:

```
sudo apt-get update
sudo apt-get install r-base r-base-dev gdebi-core
sudo su - -c "R -e \"install.packages('shiny', repos = 'http://cran.rstudio.com/')\""
sudo su - -c "R -e \"install.packages('rmarkdown', repos = 'http://cran.rstudio.com/')\""
wget https://download3.rstudio.org/ubuntu-12.04/x86_64/shiny-server-1.5.0.831-amd64.deb
sudo gdebi shiny-server-1.5.0.831-amd64.deb
```

For other platforms check [this reference](https://www.rstudio.com/products/shiny/download-server/).

We will also use a local database to store our datasets. On your local machine:

```
initdb -D db
pg_ctl -D db -l logfile start
createdb sf_opendata_insights
```

### Installing


## Deployment


## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used

## Contributing

The best way is to send a pull request.

## Versioning


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
