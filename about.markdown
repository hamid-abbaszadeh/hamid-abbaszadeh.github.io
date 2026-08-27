---
layout: page
title: About
permalink: /about/
---


https://www.index.dev/blog/advanced-cpp-coding-challenges
https://towardsdev.com/120-advanced-cpp-interview-questions-for-senior-developers-2026-33a169656d66

https://www.geeksforgeeks.org/cpp/c-programming-multiple-choice-questions/
https://www.geeksforgeeks.org/dsa/geeksforgeeks-practice-best-online-coding-platform/
https://www.geeksforgeeks.org/explore?sortBy=submissions&itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=practice_header
project:
Linux-inter-process-communication-IPC-
Dynamic-Menu-implementation-with-Binary-tree
ISO8583
OpenSSL 
tc command 

topics:
docker and containers
snapshot core dummy
cmake
systemd discription
linux 
package managers
versioning
dependency management
journalctl 
systemctl 

concept of ipc layes and websokcet  ssh tcp Frp (Fast Reverse Proxy) - Best Overall
AWS IoT Secure Tunneling Local Proxy Reference Implementation in C++
mqtt 
unit test
checking dependencies of exec filewith ldd command


git config --global --list
git config --global user.name "Hamid Abbaszadeh"               
 git config --global user.email hamid.abbaszadeh@zoi.tech     
/////////////////////////////////////////////////////////////////////////////////////
 git status                                                     
 git diff                                                       
 git status 
create a new branch :                                                    
 git switch -c bugfix/windows-string-view-conversion            
 git status   
add commit config :                                                 
 git commit -am "ensure string view is converted correctly"     
 git config --global user.name "Hamid Abbaszadeh"               
 git config --global user.email hamid.abbaszadeh@zoi.tech       
 git commit -am "ensure string view is converted correctly"   

pushing the commit:  
 git push -u origin bugfix/windows-string-view-conversion       


rollback because we commit sth wrong:
 git checkout dev -- service_client_clr/                        
 git diff                                                       
 git status                                                     
 git commit                                                     
 git push                                                       
 git status                                                     
 git commit                                                     
 git commit                                                     
 git push                                                       


git stash           --------> copy to stash
git checkout develop
git checkout -b feature/device-update-service    --->     create new branch
git stash pop        ------>past from stash
git pull                 -------> pull new branch on server
git checkout  feature/device-update-service    --->     get from my branch


https://stackoverflow.com/questions/9688200/difference-between-shared-objects-so-static-libraries-a-and-dlls-so

Debug with gdb tools
add -g in makeslm file
$gdb webvru
(gdb)run
(gdb)b main    ----> breakpoint in main
(gdb)b 120      ----->breakpoint in line 120
(gdb)b 130
(gdb)next
(gdb)print var   ----->print a var
(gdb)step      ------->going inside func 
(gdb)quite