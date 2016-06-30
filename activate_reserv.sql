create or alter procedure AF_ACTIVATE_RESERV
as
declare variable ARID integer;
declare variable WORKPEERS integer;
begin
  for select ar.arid from astrule ar into :ARID do
  begin
     select count(*) from astrulepeer arp
     join astpeertest(15) apt on (apt.apname = arp.aspeer or arp.aspeergrp=apt.apgroup)
     where arp.asruleid = :ARID
     and apt.apstate<>'FAIL' and apt.apstate<>'INACTIVE'
     and not coalesce(arp.aschans,'') containing 'r'
     into :WORKPEERS;
     if (:WORKPEERS>0) then
     begin
        /*remove reserv*/
        update astrulepeer arp set arp.ascomment=arp.asruleid,
        arp.asruleid=null where arp.asruleid=:ARID
        and coalesce(arp.aschans,'') containing 'r';
     end
     else
     begin
        /*return reserv*/
        update astrulepeer arp set
        arp.asruleid=arp.ascomment where arp.ascomment=:ARID
        and coalesce(arp.aschans,'') containing 'r';
     end
  end
end

