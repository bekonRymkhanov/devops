import curses
from curses import wrapper
import math
import subprocess
import time

output = subprocess.check_output('awk -F: \'$3 >= 1000 && $1 != "nobody" { print $1 }\' /etc/passwd', shell=True,
                                 text=True)
users = output.splitlines()
print(users)
blocked_users = []
# for i in users:

#   command = f'sudo -S passwd -S {i}'
#  process = pexpect.spawn(command,timeout=5)
# process.expect(pexpect.EOF)
# output = process.before.decode('utf-8')
#  status = output.splitlines()
# print(status)
# first_line = status[0]
# parts = first_line.split()
# status_flag = parts[1]
# if status_flag == 'L':
# blocked_users.append(i)


print(len(users))
print(float(len(users) / 4))
print(math.ceil(float(len(users) / 4)))


def main(stdscr):
    isSudo = False
    pages = math.ceil(float(len(users) / 4))
    current_arrow = 6
    current_page = 1
    curses.curs_set(0)
    last_symbol = ""
    while isSudo == False:
        curses.echo()
        stdscr.addstr(1, 0, "write your sudo password: ")
        stdscr.refresh()
        sudo = stdscr.getstr().decode("utf-8")
        result = subprocess.call('echo {} | sudo -S {}'.format(f'{sudo}', f"sudo -S -v"), shell=True)
        # stdscr.addstr(2,0, str(result))
        stdscr.clear()
        curses.noecho()
        if result == 0:
            isSudo = True
        else:
            sudo = ""
            stdscr.addstr(4, 0, "UNCORRECT")
            while True:
                stdscr.clear()
                stdscr.addstr(2, 0, "Wrond Password")
                stdscr.addstr(8, 0, "Press R to retype password")
                key = stdscr.getch()
                if key == ord("r"):
                    stdscr.clear()
                    break

    for i in users:
        output = subprocess.check_output(f"sudo passwd -S {i}", shell=True, text=True)
        status = output.splitlines()
        first_line = status[0]
        parts = first_line.split()
        status_flag = parts[1]
        if status_flag == 'L':
            blocked_users.append(i)

    while isSudo:
        stdscr.clear()
        stdscr.addstr(0, 0, '--------------------------------------------')
        stdscr.addstr(1, 0, '           User Management')
        stdscr.addstr(2, 0, '--------------------------------------------')
        stdscr.addstr(4, 0, f'page {current_page} of {pages}')
        for i, user in enumerate(users[(current_page * 4) - 4:current_page * 4]):
            status_user = "U"
            for us in blocked_users:
                if us == user:
                    status_user = "L"

            if i + 6 != current_arrow:
                stdscr.addstr(i + 6, 0, f"  {i + (current_page * 4) - 4 + 1} {user}     {status_user}")
            else:
                stdscr.addstr(i + 6, 0, f"> {i + (current_page * 4) - 4 + 1} {user} {status_user}", curses.A_REVERSE)

        stdscr.addstr(11, 0, "[↑ ↓] navigate")
        stdscr.addstr(12, 0, "[← →] page")
        stdscr.addstr(13, 0, "[N] new user")
        stdscr.addstr(14, 0, "[Q] quit")
        stdscr.addstr(15, 0, "[Backspace] delete user")
        stdscr.addstr(16, 0, "[L] lock user")
        stdscr.addstr(17, 0, "[U] unlock user")
        if last_symbol == "yB":
            stdscr.addstr(20, 0, "user del successfully")
        elif last_symbol == "yc":
            stdscr.addstr(20, 0, "deletion canceled")
        elif last_symbol == "yN":
            stdscr.addstr(20, 0, "created successfully")
        elif last_symbol == "yNc":
            stdscr.addstr(20, 0, "creation canceled")
        elif last_symbol == "yL":
            stdscr.addstr(20, 0, "locked successfully")
        elif last_symbol == "yLc":
            stdscr.addstr(20, 0, "blocking canceled")
        elif last_symbol == "yU":
            stdscr.addstr(20, 0, "unlocked successfully")
        elif last_symbol == "yUc":
            stdscr.addstr(20, 0, "unlocking canceled")
        elif last_symbol == "exist already":
            stdscr.addstr(20, 0, "this user already exist")
        elif last_symbol == "user already locked":
            stdscr.addstr(20, 0, "user already locked")
        elif last_symbol == "user not locked":
            stdscr.addstr(20, 0, "user wasnt locked")
        key = stdscr.getch()
        if key == curses.KEY_UP:
            if (current_arrow == 6):
                if current_page > 1:
                    current_page = current_page - 1
                    current_arrow = 9
            else:
                current_arrow = max(6, current_arrow - 1)
        elif key == curses.KEY_DOWN:
            if current_arrow < 9:
                if current_page == pages:
                    tmp = pages * 4 - len(users)
                    if tmp == 0:
                        if current_arrow < 9:
                            current_arrow = current_arrow + 1
                    elif tmp == 1:
                        if current_arrow < 8:
                            current_arrow = current_arrow + 1
                    elif tmp == 2:
                        if current_arrow < 7:
                            current_arrow = current_arrow + 1
                # elif tmp == 3:
                else:
                    current_arrow = current_arrow + 1
            else:
                if current_arrow == 9:
                    if current_page < pages:
                        current_page = current_page + 1
                        current_arrow = 6

        elif key == curses.KEY_RIGHT:
            if current_page < pages:
                current_arrow = 6
                current_page = current_page + 1
        elif key == curses.KEY_LEFT:
            if current_page > 1:
                current_arrow = 6
                current_page = current_page - 1
        elif key == ord('n'):
            curses.echo()
            stdscr.addstr(20, 0, "write username of your newuser: ")
            new_user = stdscr.getstr().decode("utf-8")
            if new_user in users:
                last_symbol = "exist already"
                continue
            stdscr.addstr(20, 0, "are you sure about new user? type y or n: ")
            flag = stdscr.getstr().decode("utf-8")
            if flag == "y":
                last_symbol = "yN"
                users.append(new_user)
                # command_add = 'echo PASSWORD | sudo -S useradd -m -p "" {new_user}'
                # process = pexpect.spawn(command_add)
                # process.expect(pexpect.EOF)
                subprocess.call(f"sudo useradd -m -p pass {new_user}", shell=True)
                if len(users) % 4 == 1:
                    pages = pages + 1
            else:
                last_symbol = "yNc"
            curses.noecho()
        elif key == curses.KEY_BACKSPACE:
            # while True:
            # stdscr.addstr(22, 0, f"Current Arrow Value: :{users[current_arrow-6]}")
            # stdscr.refresh()

            if users[(current_arrow - 6) + (current_page * 4) - 4] == "bekarys":
                pass
            else:
                curses.echo()
                stdscr.addstr(20, 0, "are you sure want to delete? type y or n: ")
                flag = stdscr.getstr().decode("utf-8")
                if flag == "y":
                    last_symbol = "yB"
                    subprocess.call(f"sudo userdel -r {users[(current_arrow - 6) + (current_page * 4) - 4]}",
                                    shell=True)
                    users.remove(users[(current_arrow - 6) + (current_page * 4) - 4])
                    current_arrow = current_arrow - 1
                    if len(users) % 4 == 0:
                        pages = pages - 1
                        current_page = current_page - 1
                        current_arrow = 6
                else:
                    last_symbol = "yc"
                curses.noecho()
        elif key == ord('l'):
            if users[(current_arrow - 6) + (current_page * 4) - 4] in blocked_users:
                last_symbol = "user already locked"
                continue
            if users[(current_arrow - 6) + (current_page * 4) - 4] == "bekarys":
                pass
            else:
                curses.echo()
                stdscr.addstr(20, 0, "are you sure want to block? type y or n: ")
                flag = stdscr.getstr().decode("utf-8")
                if flag == "y":
                    last_symbol = "yL"
                    subprocess.call(f"sudo usermod -L {users[(current_arrow - 6) + (current_page * 4) - 4]}",
                                    shell=True)
                    blocked_users.append(users[(current_arrow - 6) + (current_page * 4) - 4])
                else:
                    last_symbol = "yLc"
                curses.noecho()
        elif key == ord('u'):
            if users[(current_arrow - 6) + (current_page * 4) - 4] in blocked_users:
                pass
            else:
                last_symbol = "user not locked"
                continue
            curses.echo()
            stdscr.addstr(20, 0, "are you sure want to block? type y or n: ")
            flag = stdscr.getstr().decode("utf-8")
            if flag == "y":
                last_symbol = "yU"
                subprocess.call(f"sudo usermod -U {users[(current_arrow - 6) + (current_page * 4) - 4]}", shell=True)
                blocked_users.remove(users[(current_arrow - 6) + (current_page * 4) - 4])
            else:
                last_symbol = "yUc"
            curses.noecho()
        elif key == ord('q'):
            subprocess.call("sudo -k", shell=True)
            break

    stdscr.refresh()


wrapper(main)