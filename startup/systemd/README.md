# Creating systemd Services for VinlyPi

Create the service files in `/etc/systemd/system` and copy the contents in.

```sh
sudo nano /etc/systemd/system/vinlypi.service
sudo nano /etc/systemd/system/vinlypi-rfid.service
```

Then update the permissions of the service files.

```sh
sudo chmod 644 /etc/systemd/system/vinlypi.service
sudo chmod 644 /etc/systemd/system/vinlypi-rfid.service
```

Reload the systemd daemon

```sh
sudo systemctl daemon-reload
```

Enable the services to start on boot

```sh
sudo systemctl enable vinlypi.service
sudo systemctl enable vinlypi-rfid.service
```
