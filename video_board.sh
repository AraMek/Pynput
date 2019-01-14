HOST='192.168.8.172'

raspivid -n -w 640 -h 360 -b 4500000 -fps 30 -vf -hf -t 0 -cd MJPEG -o - | \
gst-launch-1.0 -v \
	rtpbin name=rtpbin latency=200 drop-on-latency=true buffer-mode=4 ntp-time-source=3 ntp-sync=true rtcp-sync-send-time=false  \
	fdsrc ! jpegparse ! rtpjpegpay ! queue ! rtpbin.send_rtp_sink_0  \
	rtpbin.send_rtp_src_0 ! udpsink port=5000 host=$HOST sync=true async=false \
	rtpbin.send_rtcp_src_0 ! udpsink port=5001 host=$HOST sync=false async=false \
	udpsrc port=5005 caps="application/x-rtcp" ! rtpbin.recv_rtcp_sink_0
