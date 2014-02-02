# run apt-get update 
exec { 'apt-get update':
  command => '/usr/bin/apt-get update',
}

package { 'python-software-properties':
    require => Exec['apt-get update'],
    ensure => present
}

exec { 'install rethink':
    require => Package['python-software-properties'], 
    command => '/usr/bin/add-apt-repository ppa:rethinkdb/ppa &&  /usr/bin/apt-get update &&  /usr/bin/apt-get -y install rethinkdb'
}

Package { ensure => present }

$aptpackages = ['git','vim','tmux','python-pip','python-dev','curl','ipython']
$pippackages = ['flask','requests','rethinkdb']

package { $aptpackages:
    require => [ Exec['apt-get update'] ],
  }

package { $pippackages:
    require => [ Package[$aptpackages], Exec['install rethink'] ],
    provider => pip,
}
