clear all;
behave_dir = '/Users/drdj/Box Sync/data_visualizations/react/';
subid = input('What is the subject id? :', 's');

%may have to change below to the following if using subject numbers instead
%of strings: file = [subid num2str '.txt] -- may also have to remove '.txt'
file = [behave_dir subid];

fidread = fopen(file);


count = 0;


numpics = 180;
reactpics = 150;
numcon = 3;
grouparray=[];

while count < numpics;
 
 readline = fgetl(fidread); %read each line
    
  
   if length(readline) < 1;
       continue;
   end
tabs = findstr(readline,sprintf('\t'));  
      
           count = count + 1;      
                      
           x{count} = readline((1):tabs(1));
           y{count} = readline(tabs(1):length(readline));

      end
      
          
          
barray = [cellfun(@str2num,x') cellfun(@str2num,y')]; %x and y coordinates of b

count = 0;
i = 0;
j = 0;
k = 0;
n = 0;

while count < (numpics*2) + ((numpics*2)/3) + reactpics;
    
    readline = fgetl(fidread);
    
     if length(readline) < 1;
       continue;
     end
tabs = findstr(readline,sprintf('\t'));
     count = count + 1;
     
     if count <= numpics;
     i = i + 1;
     
     bt1pic{i} = readline((1):tabs(1)-1);
     bt1x{i} = readline(tabs(1)+1:tabs(2)-1);
     bt1y{i} = readline(tabs(2)+1:tabs(3)-1);
     bt1rt{i} = readline(tabs(3)+1:length(readline));
     %end of day 1
     
     elseif count > numpics && count <= numpics + reactpics;
                   
        k = k + 1;
        reactpic{k} = readline((1):tabs(1)-1);
        reactcon{k} = readline(tabs(1):length(readline));
     
     
     elseif count > numpics + reactpics && count <= reactpics + ((numpics*5)/3);
         j = j + 1;
     
     rpic{j} = readline((1):tabs(1)-1);
     rx{j} = readline(tabs(1)+1:tabs(2)-1);
     ry{j} = readline(tabs(2)+1:tabs(3)-1);
     rrt{j} = readline(tabs(3):length(readline));
      
     else
          
         n = n + 1;
     
     bt2pic{n} = readline((1):tabs(1)-1);
     bt2x{n} = readline(tabs(1)+1:tabs(2)-1);
     bt2y{n} = readline(tabs(2)+1:tabs(3)-1);
     bt2rt{n} = readline(tabs(3)+1:length(readline));    
           
         
     end
      
end

fclose(fidread);

bt1array = [cellfun(@str2num,bt1pic') cellfun(@str2num,bt1x') cellfun(@str2num,bt1y') cellfun(@str2num,bt1rt')]; %B final test 1 array
reactarray = [cellfun(@str2num,reactpic') cellfun(@str2num,reactcon')];                                 %all reactivated items
rarray = [cellfun(@str2num,rpic') cellfun(@str2num,rx') cellfun(@str2num,ry') cellfun(@str2num,rrt')]; %Reactivation Retrieval array
bt2array = [cellfun(@str2num,bt2pic') cellfun(@str2num,bt2x') cellfun(@str2num,bt2y') cellfun(@str2num,bt2rt')]; %C final test 1 array

for i=1:length(bt1array)
    bt1array(i,5)=i;
    bt2array(i,5)=i;
    if i<=length(rarray)
        rarray(i,5)=i;
    end
end

%may have to add '.txt'?
file2 = [behave_dir subid 'allarray'];

fidread = fopen(file2);

count = 0;

while count < numpics;
 
 readline = fgetl(fidread); %read each line
    
  
   if length(readline) < 1;
       continue;
   end
tabs = findstr(readline,sprintf('\t'));  %specify what tabs are in txt file
      
           count = count + 1;      
           
           grouppic{count} = readline((1):tabs(1));
           group{count} = readline(tabs(2):length(readline));

      end
      
          
          
grouparray = [cellfun(@str2num,grouppic') cellfun(@str2num,group')]; %pic # and group assignment
fclose(fidread);

%grouparray contains the following: 
% 1 - Pic ID
% 2 - Condition ID (1 = RR, 2 = RC, 3 = NR)
% 3 - BX coord
% 4 - BY coord
% 5 - BT1X coord
% 6 - BT1Y coord
% 7 - BT2X coord
% 8 - BT2Y coord
% 9 - RX coord
% 10 - RY coord
%%%% 11 - react order
% 11 - bt1 RT
% 12 - React RT
% 13 - Bt2 RT
% 14 - bt1 order
% 15 - React order
% 16 - Bt2 order

    
for i = 1:numpics
    j = 1;
        while j <= numpics
        
            if grouparray(i,1) == j
            grouparray(i,3) = barray(j,1);
            grouparray(i,4) = barray(j,2);  
            end
            if grouparray(i,1) == bt1array(j,1)
               grouparray(i,5) = bt1array(j,2);
               grouparray(i,6) = bt1array(j,3);
               grouparray(i,11) = bt1array(j,4);
               grouparray(i,14) = bt1array(j,5);
               
            end   
            if grouparray(i,1) == bt2array(j,1)
               grouparray(i,9) = bt2array(j,2);
               grouparray(i,10) = bt2array(j,3);   
               grouparray(i,13) = bt2array(j,4);   
               grouparray(i,16) = bt2array(j,5);   

            end
%             if j <= reactpics;
%                 if grouparray(i,1) == reactarray(j,1);
%                 grouparray(i,11) = j;
%                 end
%             end
            
             if j <= (2*(numpics/3))
               
                if grouparray(i,1) == rarray(j,1)
                   grouparray(i,7) = rarray(j,2);
                   grouparray(i,8) = rarray(j,3);
                   grouparray(i,12) = rarray(j,4);
                   grouparray(i,15) = rarray(j,5);
                   
                end 
             end
            j = j + 1;
        end
end

fname = 'react_raw.csv';
% fid = fopen(fname, 'w');
% fprintf(fid, '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s', 'sub', 'cond', 'x', 'y', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 't1_rt', 't2_rt', 't3_rt', 't1_order', 't2_order', 't3_order');
fid = fopen(fname, 'a');


for i = 1:length(grouparray)
   fprintf(fid, '\n');
   fprintf(fid, '%s\t', subid);
   fprintf(fid, '%d\t', grouparray(i,2:end));
end
fclose(fid);
