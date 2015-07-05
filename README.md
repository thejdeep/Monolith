# Monolith
YUM plugin that takes snapshots and does rollbacks of root FS on BTRFS

## Installation 
```
$ git clone https://github.com/thejdeep/Monolith.git
$ cd Monolith/
$ sudo cp monolith.py /usr/lib/yum-plugins/
$ sudo cp monolith.conf /etc/yum/pluginconf.d/
```

## Usage

To take snapshot of the root file system
```
$ sudo yum snapshot <snap_name>
```
To rollback to a previous snapshot
```
$ sudo yum rollback <snap_name>
```

