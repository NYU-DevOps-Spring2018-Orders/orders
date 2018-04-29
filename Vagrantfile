# -*- mode: ruby -*-
# vi: set ft=ruby :

# 2 for backwards compatibility
Vagrant.configure(2) do |config|

    config.vm.box = "ubuntu/xenial64"

    # set up network ip and port forwarding
    config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
    config.vm.network "private_network", ip: "192.168.33.10"

    config.vm.provider "virtualbox" do |vb|
      # Customize the amount of memory on the VM:
      vb.memory = "512"
      vb.cpus = 1
      # Fixes some DNS issues on some networks
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    end

    # Copy .gitconfig file so that git credentials are correct
    if File.exists?(File.expand_path("~/.gitconfig"))
      config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
    end

    # Copying ssh keys for github so that your git credentials work
    if File.exists?(File.expand_path("~/.ssh/id_rsa"))
      config.vm.provision "file", source: "~/.ssh/id_rsa", destination: "~/.ssh/id_rsa"
    end

    # Change the permission of files and directories
    # so that nosetests runs without extra arguments.
    config.vm.synced_folder ".", "/vagrant", mount_options: ["dmode=775,fmode=664"]

    # Provisioning for Python and Bluemix
    config.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y git python-pip python-dev build-essential
      pip install --upgrade pip
      apt-get -y autoremove

      echo "\n******************************"
      echo " Installing Bluemix CLI"
      echo "******************************\n"
      wget -q -O - https://clis.ng.bluemix.net/download/bluemix-cli/latest/linux64 | tar xzv
      cd Bluemix_CLI/
      ./install_bluemix_cli
      cd ..
      rm -fr Bluemix_CLI/
      bluemix config --usage-stats-collect false

      # Make vi look nice
      sudo -H -u ubuntu echo "colorscheme desert" > ~/.vimrc

      # Install PhantomJS for Selenium browser support
      echo "\n***********************************"
      echo " Installing PhantomJS for Selenium"
      echo "***********************************\n"
      sudo apt-get install -y chrpath libssl-dev libxft-dev
      # PhantomJS https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
      cd ~
      export PHANTOM_JS="phantomjs-1.9.7-linux-x86_64"
      #export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64"
      wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS.tar.bz2
      sudo tar xvjf $PHANTOM_JS.tar.bz2
      sudo mv $PHANTOM_JS /usr/local/share
      sudo ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin
      rm -f $PHANTOM_JS.tar.bz2

      # Install app dependencies

      cd /vagrant
      sudo pip install -r requirements.txt
    SHELL

    # Add PostgreSQL docker container
    config.vm.provision "shell", inline: <<-SHELL
      # Prepare PostgreSQL data share
      sudo mkdir -p /var/lib/postgresql/data
      sudo chown vagrant:vagrant /var/lib/postgresql/data
    SHELL

    config.vm.provision "docker" do |d|
      d.build_image "/vagrant/docker",
        args: "-t postgres"
      d.run "postgres",
        args: "-d --name postgres -p 5432:5432 -v /var/lib/postgresql/data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=passw0rd -d postgres"
    end

    # Add PostgreSQL tables
    config.vm.provision "shell", inline: <<-SHELL
      docker exec -it postgres psql -U postgres -c "DROP TABLE test;"
      docker exec -it postgres psql -U postgres -c "DROP TABLE development;"
      docker exec -it postgres psql -U postgres -c "CREATE DATABASE test;"
      docker exec -it postgres psql -U postgres -c "CREATE DATABASE development;"
    SHELL
end
