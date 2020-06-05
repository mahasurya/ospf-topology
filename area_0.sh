perl /home/admapp/surya/ospf/run.pl t-d2-jt2 "show ospf 1 0 database router" > /home/admapp/surya/ospf/DB_0
python3 /home/admapp/surya/ospf/ospf_telkom_region /home/admapp/surya/ospf/DB_0 /home/admapp/surya/ospf/hostname /home/admapp/surya/ospf/OSPF_0_region.dot
dot -Kdot -Tsvg /home/admapp/surya/ospf/OSPF_0_region.dot > /var/www/html/ospf/OSPF_0_region.svg