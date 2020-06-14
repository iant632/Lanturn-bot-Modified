# Lanturn-bot-Modified
This is the modified Lanturn Bot based by fishguy6564

NEED sys-botbase and ldm_mitm

I am not good at English so my English is bad. You should change my text if you need.


>What's different from original Lanturn Bot?
* Added two Nintendo Switch support
* Added tradeList command to print the line
* Added tradeCancel command to cancel the trade
* Added CheckSeedInfo command to check the seed and simple information of shiny pokemon.
* Added reading pokemon and trainer info.
* Added reading the date and telling which date should you save.
* Added automatic recovery when the bot is offline (need ldm_mitm)
* Added 0 support in password


>How to use

0. Need Hacked Switch which installed sys-botbase and ldn_mitm(optional), Need python version over 3.8 with discord.py, z3-solver installed. (using pip install discord.py z3-solver)  

1. Write your bot's token in bot.py
2. Write your Nintendo Switch's IP in chulClient.py and chul2Client.py (if you have two Nintendo Switch)
3. Run both chul1off.py and chul2off.py
4. Run chul1on.py if you use chulClient.py.
5. Run chul2on.py if you use chul2Client.py.
6. Run run.bat, chul1.bat, chul2.bat

>How to control two Nintendo Switch

The bot will detect first 2 bytes in com.bin  
0x0 : Check Nintendo Switch 1  
0x1 : Check Nintendo Switch 2  

If you run chul1on.py, then byte in 0x0 will change into 1. That means Nintendo Switch 1 is online.  
If you run chul1off.py, then it will change into 0. That means Nintendo Switch 1 is offline.

The same applies to chul2on.py, chul2off.py except it will change 0x1 instead of 0x0.

You can change the status of the Switch freely while running the bot. 
