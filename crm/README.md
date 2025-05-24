[Profile Tools](../)
# SuiteCRM - Partner Database for Azure

<!-- Under Development - SQL table CREATE script for Azure -->

[SuiteCRM](https://SuiteCRM.com) provides a standardized partner admin [database schema](https://schema--suitecrm-docs.netlify.app/schema) with a [large developer community](https://community.SuiteCRM.com).

Help us automate including PHP and a remote Azure database init within our start.sh install steps...

1. [Download SuiteCRM version 8.7.1](https://suitecrm.com/wpfd_file/suitecrm-8-7-1/) and unzip in your webroot.  
There are [more recent versions](https://suitecrm.com/download/), but we're matching the version in our .sh file for now.

2. Rename the folder to **SuiteCRM**

3. [Get our .sh fork for Mac and Windows - SuiteCRM 8.7.1](https://github.com/ModelEarth/SuiteCRM_Script/blob/main/SCRM_8.7.1_0.1.4_MacLinuxWindows.sh)  
The .sh script was initially developed by Chris for his 10-minute [Linux install](https://github.com/motaviegas/SuiteCRM_Script) .sh file [video and steps](https://community.suitecrm.com/t/how-to-install-suitecrm-8-6-1-under-10-minutes/93252).  

4. Place the .sh file in your local SuiteCRM folder and rename the file to **start.sh**

## Quick install script for Mac, Linux and Windows

[Collaborate with us](/dreamstudio/earth/) using standardized data tables within Microsoft Azure, SQL Express and MariaDB.
Summary of what's included for each OS within the start.sh script

| OS      | PHP            | Apache        | DB Option                     |
|---------|----------------|---------------|-------------------------------|
| <a href="#mac">MacOS</a>   | via brew       | via brew      | MariaDB                       |
| <a href="#linux">Linux</a>   | via apt        | via apt       | MariaDB                       |
| <a href="#windows">Windows</a> | via Chocolatey | via Chocolatey| SQL Express / Azure / MariaDB |

<br>
## 10-Minute SuiteCRM Setup

Open a terminal in your SuiteCRM folder and grant the start.sh file (from above) permission within the folder:

	sudo chmod +x ./start.sh

<!--
	Not from video, probably don't need.
	sudo chmod -R 755 .
-->

As you run the start.sh install, also follow the [steps below video](https://community.suitecrm.com/t/how-to-install-suitecrm-8-6-1-under-10-minutes/93252).

Including "sudo" below before `./start.sh` may not be needed.
The http server currently gets deactivated AFTER php portion regardless of sudo on MacOS.  
Please document how to include permissions for PHP.

	sudo ./start.sh

<!--
Will sudo be needed if php was installed previously?
We could provide an option to avoid sudo here, with additional manual steps below.
-->

Take note of the user and password of the MariaDB database that will be requested.

**MacOS users** - You may need to run these if you have brew errors:

	brew install --cask temurin

	# Not sure if these two cmds needed
	brew untap homebrew/cask-versions
	brew untap AdoptOpenJDK/openjdk

	brew uninstall --cask adoptopenjdk13
	brew uninstall python@3.8


For Error: Permission denied @ apply2files - /usr/local/lib/docker/cli-plugins
Deleting the folder was necessary (better than adding user permissions on Docker folder)

	sudo rm -rf /usr/local/lib/docker
	brew cleanup

Don't install Docker with Homebrew. 
Docker for Mac (Docker Desktop) provides better performance and integration with the operating system. 


If you installed ImageMagick via Homebrew (which is common), you can safely press Enter to accept [autodetect], because the script will usually find it in the standard Homebrew location. Or use `brew --prefix imagemagick` to find it.

**From the steps below the video:**

[View steps](https://community.suitecrm.com/t/how-to-install-suitecrm-8-6-1-under-10-minutes/93252).

When the .sh script finishes successfully, run the cmd:<!-- sudo mysql_secure_installation -->

	sudo mariadb-secure-installation

The older name for the cmd above was: mysql_secure_installation

First enter your machine password, then blank for the MariaDB database's root password

Initial login response says:
You already have your root account protected, so you can safely answer 'n'.

However the steps under [the 10-minute video](https://community.suitecrm.com/t/how-to-install-suitecrm-8-6-1-under-10-minutes/93252) are:
Switch to unix_socket authentication [Y/n] y
Change the root password? [Y/n] y
put your DB root password and take note of it!!!
Remove anonymous users? [Y/n] y
Disallow root login remotely? [Y/n] y
Remove test database and access to it? [Y/n] y
Reload privilege tables now? [Y/n] y

**IP retrieved**
Get your "IP retrieved" near the start of your start.sh terminal.

**Webroot at localhost:8080**
The Apache port for Homebrew says "It works!"  
But broke (stopped) when running the PHP install portion.

[http://localhost:8080](http://localhost:8080)

## PHP Site Activation
 
Please document steps that work for you by posting an issue in our [profile repo](https://github.com/ModelEarth/profile/tree/main/crm), or fork and send a PR.

The first time you may need to run `./start.sh` again - if the database did not initially exist.

BUG: When running a second time, the webroot stopped working.

Probable cause(s) - These appear right before "Installing MariaDB":
PHP module not found. PHP may not work correctly with Apache.
✅ PHP handler configuration added.
✅ Directory listing disabled.


## To Try for PHP...

    brew services start php@8.2

To enable PHP in Apache add the following to httpd.conf and restart Apache:
    LoadModule php_module /usr/local/opt/php@8.2/lib/httpd/modules/libphp.so

    <FilesMatch \.php$>
        SetHandler application/x-httpd-php
    </FilesMatch>

Finally, check DirectoryIndex includes index.php
    DirectoryIndex index.php index.html

The php.ini and php-fpm.ini file can be found in:
    /usr/local/etc/php/8.2/

php@8.2 is keg-only, which means it was not symlinked into /usr/local,
because this is an alternate version of another formula.

If you need to have php@8.2 first in your PATH, run:
  echo 'export PATH="/usr/local/opt/php@8.2/bin:$PATH"' >> ~/.zshrc
  echo 'export PATH="/usr/local/opt/php@8.2/sbin:$PATH"' >> ~/.zshrc

For compilers to find php@8.2 you may need to set:
  export LDFLAGS="-L/usr/local/opt/php@8.2/lib"
  export CPPFLAGS="-I/usr/local/opt/php@8.2/include"

To start php@8.2 now and restart at login:

    brew services start php@8.2

Or, if you don't want/need a background service you can just run:

    /usr/local/opt/php@8.2/sbin/php-fpm --nodaemonize

🔧 Updating PATH to use PHP 8.2...
Linking /usr/local/Cellar/php@8.2/8.2.28_1... 25 symlinks created.

If you need to have this software first in your PATH instead consider running:

    echo 'export PATH="/usr/local/opt/php@8.2/bin:$PATH"' >> ~/.zshrc
    echo 'export PATH="/usr/local/opt/php@8.2/sbin:$PATH"' >> ~/.zshrc


<!--
TODO: Create a get.sh file that automatically pulls the .sh file from GitHub, saves, renames to start.sh and runs the script.
-->
<br id="mac">

# MacOS - SuiteCRM Install

This script automates the installation and configuration of SuiteCRM 8.7.1 on macOS environments. It handles the complete setup process including web server, database, and application deployment.

## Prerequisites

- macOS operating system (compatible with both Intel and Apple Silicon Macs)
- Regular user account (do not run as root)
- Internet connection for downloading packages

## Components Installed

- **Homebrew**: Package manager for macOS
- **Apache HTTP Server**: Web server to host SuiteCRM
- **PHP 8.2**: Required programming language for SuiteCRM
- **MariaDB**: Database server for storing CRM data
- **SuiteCRM 8.7.1**: The CRM application itself

## Installation Process

### System Preparation
- Checks against running as root (for security)
- Installs Homebrew if not present
- Updates and upgrades existing Homebrew packages

### Software Installation
- Installs essential tools (wget, unzip)
- Installs or updates PHP 8.2
- Installs and configures Apache HTTP Server
- Installs and starts MariaDB database server

### Apache Configuration
- Configures Apache to use port 8080 (Homebrew default)
- Enables required modules (rewrite, headers)
- Configures PHP integration with Apache
- Sets up virtual hosts
- Implements security headers:
  - X-Content-Type-Options
  - X-XSS-Protection
  - X-Frame-Options

### PHP Configuration
- Sets optimal PHP parameters:
  - Memory limit: 512M
  - Upload max filesize: 50M
  - Post max size: 50M
  - Max execution time: 300 seconds
  - Disables error display and PHP version exposure

### Database Setup
- Creates a CRM database with UTF-8 Unicode support
- Creates a database user with appropriate privileges
- Verifies database and user creation

### SuiteCRM Installation
- Downloads SuiteCRM 8.7.1
- Extracts files to the configured document root
- Sets appropriate file and directory permissions
- Makes console scripts executable
- Ensures storage and cache directories are writable

## Security Measures

- Disables directory listing in Apache
- Sets secure file permissions (750 for directories, 640 for files)
- Implements HTTP security headers
- Provides reminder to run `mysql_secure_installation`

## Post-Installation

### Verification
- Creates a health check PHP file
- Restarts Apache and MariaDB services
- Verifies that services are running correctly

### Accessing SuiteCRM
- SuiteCRM will be available at: http://[your-server-ip]:8080
- Health check URL: http://[your-server-ip]:8080/health.php

## Platform-Specific Notes

- Automatically detects and configures for either Intel or Apple Silicon Macs
- Uses appropriate paths based on the architecture:
  - Apple Silicon: `/opt/homebrew/...`
  - Intel: `/usr/local/...`
- Creates backups of all configuration files before modifications

## Troubleshooting

If you encounter issues during installation:
- Check Apache logs: `/opt/homebrew/var/log/httpd/` or `/usr/local/var/log/httpd/`
- Verify MariaDB is running: `brew services list`
- Ensure permissions are set correctly for the CRM directory
- Verify PHP integration with Apache is working correctly

## Security Recommendations

- Run `mysql_secure_installation` to secure your MariaDB installation
- Consider setting up SSL for production environments
- Review Apache and PHP configurations for additional security hardening
- Regularly update all components with `brew update` and `brew upgrade`

<br id="linux">

# Linux - SuiteCRM Install

A comprehensive installation script for automatically deploying SuiteCRM 8.7.1 on Linux systems (Ubuntu/Debian). Includes system updates, required dependencies, database configuration, web server setup, and security hardening.

## Prerequisites

- A fresh installation of Ubuntu/Debian Linux
- Root/sudo access
- Internet connectivity to download packages

## Full Stack Installation

- PHP 8.2 with required extensions
- Apache web server
- MariaDB database server
- SuiteCRM 8.7.1

## Security Enhancements

- Apache directory listing disabled
- Optimized file permissions
- Security headers configuration
- Firewall setup (if UFW is available)
- PHP security settings

## Performance Optimization

- Tuned PHP configuration (memory limits, execution time)
- Optimal file permissions

## Verification Steps

- Database creation verification
- Database user verification
- Permissions validation
- Health check page

## Usage

1. Download the setup script
2. Make the script executable: `chmod +x setup.sh`
3. Run with sudo privileges: `sudo ./setup.sh`

## Post-Installation Tasks

After successful installation:

1. Run `mysql_secure_installation` to secure your MariaDB installation
2. Complete the SuiteCRM web-based setup by navigating to `http://YOUR_SERVER_IP`
3. Verify the installation with the health check: `http://YOUR_SERVER_IP/health.php`

## Configuration Details

- **Web Server**: Apache with mod_rewrite and security headers
- **Database**: MariaDB with dedicated CRM database and user
- **PHP**: Version 8.2 with optimized settings:
  - 512MB memory limit
  - 50MB upload file size
  - 300 seconds max execution time
  - Production-ready error settings

## Troubleshooting

The script includes extensive error handling and will provide specific error messages if any step fails. Common issues may include:

- Network connectivity problems
- Insufficient disk space
- Port conflicts
- Missing dependencies

## Security Notes

This installation includes basic security measures, but for production environments consider implementing:

- SSL/TLS certificates
- Regular system updates
- Database backups
- Network access restrictions
- Additional firewall rules

<br id="windows">

# Windows - SuiteCRM Install

This script automates the installation and configuration of 
SuiteCRM 8.7.1 on Windows environments using Git Bash or Cygwin.

## Prerequisites

- Windows operating system
- Git Bash or Cygwin installed
- Administrative privileges
- Chocolatey package manager

## Components Installed

- **Apache HTTP Server**: Web server to host SuiteCRM
- **PHP 8.2**: Required programming language for SuiteCRM
- **MariaDB**: Database server for storing CRM data
- **SuiteCRM 8.7.1**: The CRM application itself

## Installation Process

### System Preparation
- Checks for administrative privileges
- Verifies Chocolatey installation
- Sets up necessary paths for Apache and PHP

### Software Installation
- Installs essential tools (wget, unzip)
- Installs and configures Apache HTTP Server
- Installs and configures PHP 8.2
- Installs and starts MariaDB database server

### Apache Configuration
- Loads the PHP module in Apache configuration
- Enables required modules (rewrite, headers)
- Configures virtual hosts
- Sets security headers (XSS protection, content-type options, etc.)

### PHP Configuration
- Sets optimal PHP parameters:
  - Memory limit: 512M
  - Upload max filesize: 50M
  - Post max size: 50M
  - Max execution time: 300 seconds
  - Disables displaying errors and PHP version exposure
- Enables essential PHP extensions (curl, gd, mbstring, mysqli, pdo_mysql, soap, xml)

### Database Setup
- Creates a CRM database with UTF-8 Unicode support
- Creates a database user with appropriate privileges
- Verifies database and user creation

### SuiteCRM Installation
- Downloads SuiteCRM 8.7.1
- Extracts files to the configured document root
- Sets appropriate file permissions using Windows ACLs

### Security & Network Configuration
- Configures Windows Firewall to allow HTTP traffic (port 80)
- Sets secure file permissions
- Creates a health check file for monitoring

## Post-Installation

### Verification
- Ensures Apache is running on port 80
- Verifies MariaDB is running on port 3306
- Provides a summary of the installation with important paths and credentials

### Security Recommendations
- Run `mysql_secure_installation` to further secure MariaDB
- Review Apache and PHP configurations for production environments
- Check log files for troubleshooting:
  - Apache logs: Located in the Apache logs directory
  - MariaDB logs: Available in Windows Event Viewer

## Completing the Installation

After the script runs successfully, you can:
1. Access SuiteCRM via web browser: http://[your-server-ip]
2. Complete the web-based installation wizard
3. Verify system operation with the health check: http://[your-server-ip]/health.php

## Error Handling

The script handles various error conditions throughout the process:
- Creates backups of configuration files before modification
- Provides detailed error messages if any step fails
- Offers fallback options for certain operations

## Troubleshooting

If you encounter issues during installation:
- Check the Apache and MariaDB log files
- Verify all prerequisites are correctly installed
- Ensure you're running the script with administrative privileges
