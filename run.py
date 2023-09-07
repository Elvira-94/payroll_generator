import os
import time
import pandas as pd
import getpass
from fpdf import FPDF
from collections import defaultdict
from colorama import init, Fore

init(autoreset=True)

def clear_screen():
    os_name = os.name
    if os_name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


def start_animation():
    clear_screen()
    print(Fore.GREEN + "----------------------------------------------------------------")
    print(Fore.GREEN + "              Welcome to Jocaware Payroll System                ")
    print(Fore.GREEN + "                     Prototype (PSP)                            ")
    print(Fore.GREEN + "----------------------------------------------------------------")
    print(Fore.WHITE + "                           LOADING...                           ")
    time.sleep(3)
    clear_screen()


def exit_animation():
    clear_screen()
    print(Fore.GREEN + "----------------------------------------------------------------")
    print(Fore.GREEN + "                    Thank you for using PSP                     ")
    print(Fore.GREEN + "                  Have a Great Day Ahead!                       ")
    print(Fore.GREEN + "----------------------------------------------------------------")
    time.sleep(2)
    clear_screen()

path_to_admin_payslip_file = '/Users/elviraoredein/Desktop/payroll_generator/Employee Details.xlsx'


def main():
    start_animation()
    
    print(Fore.CYAN + "Welcome to Jocaware Payroll System Prototype (PSP)")
    credentials = {
        "Ellie":"password"
    }

    while True:
        username_input = input("Please enter Admin username: ")
        if not credentials.get(username_input, None):
            print(Fore.RED + "Invalid Username")
            continue

        password_input = getpass.getpass("Please enter Admin password: ")
        if password_input == credentials[username_input]:
            print(Fore.GREEN + "Login Successful!")   
            break 
        else:
            print(Fore.RED + "Invalid Login, please try again!")

    while True:
        command = input("\n(a) Run Payroll\n(b) Report Cumulative Totals\n(c) Modify Employees\n(d) Help\n(e) Exit\n> ")

        if command == "a":
            month = int(input("Enter month number (1-12, 0 to exit): "))

            if month == 0:
                break
            run_payroll(month)

        elif command == "b":
            report_cumulative_totals()
        elif command == "c":
            print(Fore.RED + "Modify Employees not implemented in prototype") 
        elif command == "d":
            display_help()
        elif command == "e":
            exit_animation()
            break


def run_payroll(month):
    
    employees = pd.read_excel(path_to_admin_payslip_file)
    for index, row in employees.iterrows():
        if row['Pay Period'] != month:
            continue
        gross = round(row['Hours Worked'] * row['Rate'],2)
        paye = round(gross * row['PAYE'],2)
        usc = round(gross * row['USC'],2)
        prsi = round(gross * row['EMPLOYEES PRSI'],2)
        net = round(gross - (paye + usc + prsi),2)

        employees.at[index, 'Pay Period'] = month
        employees.at[index, 'Gross'] = gross
        employees.at[index, 'Net Pay'] = net

        gross_cumulatives = defaultdict(lambda: 0)
        tax_cumulatives = defaultdict(lambda: 0)
        net_cumulatives = defaultdict(lambda: 0)

    # Loop through each row to calculate cumulative totals
    for _, emp_row in employees.iterrows():
        if emp_row['Pay Period'] <= month:
            gross_cumulatives[emp_row['Emp ID']] += emp_row['Gross']
            tax_cumulatives[emp_row['Emp ID']] += (emp_row['Gross'] - emp_row['Net Pay'])
            net_cumulatives[emp_row['Emp ID']] += emp_row['Net Pay']

    # Complete implementation would look more professional.
    for index, row in employees.iterrows():
        if row['Pay Period'] != month:
            continue
       
        pdf = FPDF()
        pdf.add_page()

        # Set consistent left margin
        pdf.set_left_margin(10)

        # Logo at the top
        pdf.image('/Users/elviraoredein/Desktop/payroll_generator/images/JocawareLogo.png', x=10, y=8, w=33)
        pdf.ln(20)  # Reduced space after logo

        # Title
        pdf.set_font("Arial", size=12, style='B')  # Reduced font size for Title
        pdf.cell(190, 6, "Employee Payslip", ln=True, align='C')  # Reduced cell height
        pdf.ln(6)  # Reduced space after title

        # Employee Details Header
        pdf.set_font("Arial", size=8)  # Reduced font size
        pdf.set_fill_color(0, 123, 255)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(190, 6, "Details:", ln=True, align='L', fill=True)
        pdf.ln(6)  # Reduced space after header

        # Employee Details Content
        pdf.set_text_color(0, 0, 0)
        pdf.cell(95, 6, f"Pay Period: {month}")
        pdf.cell(95, 6, f"Employee ID: {row['Emp ID']}", ln=True)
        pdf.cell(95, 6, f"First Name: {row['First Name ']}")
        pdf.cell(95, 6, f"Second Name: {row['Second Name']}", ln=True)
        pdf.cell(190, 6, f"Pay Group: {row['Pay Group']}", ln=True)
        pdf.cell(190, 6, f"PPS: {row['PPS']}", ln=True)
        pdf.ln(6)

        # Gross Earnings Header
        pdf.set_fill_color(0, 123, 255)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(190, 6, "Gross Earnings:", ln=True, align='L', fill=True)
        pdf.ln(6)

        # Gross Earnings Content
        pdf.set_text_color(0, 0, 0)
        pdf.cell(95, 6, f"Hours Worked: {row['Hours Worked']}")
        pdf.cell(95, 6, f"Rate: {row['Rate']}", ln=True)
        pdf.cell(190, 6, f"Gross Pay: {chr(128)}{round(float(row['Gross']), 2)}", ln=True)
        pdf.ln(6)

        # Deductions Header
        pdf.set_fill_color(0, 123, 255)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(190, 6, "Deductions:", ln=True, align='L', fill=True)
        pdf.ln(6)

        # Deductions Content
        pdf.set_text_color(0, 0, 0)
        pdf.cell(95, 6, f"PAYE: {float(row['PAYE'])*100}%")
        pdf.cell(95, 6, f"USC: {float(row['USC'])*100}%", ln=True)
        pdf.cell(95, 6, f"PRSI: {float(row['EMPLOYEES PRSI'])*100}%")
        pdf.cell(95, 6, f"Pension: NA", ln=True)
        pdf.ln(6)

        # Net Pay
        pdf.cell(190, 6, f"Net Pay: {chr(128)}{round(float(row['Net Pay']), 2)}", ln=True)
        pdf.ln(6)

        # Cumulative Totals Header
        pdf.set_fill_color(0, 123, 255)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(190, 6, "Cumulative Totals (Year to Date):", ln=True, align='L', fill=True)
        pdf.ln(6)

        # Cumulative Totals Content
        pdf.set_text_color(0, 0, 0)
        pdf.cell(95, 6, f"Cumulative Gross Pay: {chr(128)}{round(float(gross_cumulatives[row['Emp ID']]), 2)}")
        pdf.cell(95, 6, f"Cumulative Tax Deductions: {chr(128)}{round(float(tax_cumulatives[row['Emp ID']]), 2)}", ln=True)
        pdf.cell(190, 6, f"Cumulative Net Pay: {chr(128)}{round(float(net_cumulatives[row['Emp ID']]), 2)}", ln=True)
        pdf.ln(6)

        # Footer
        pdf.set_y(-31)
        pdf.set_font("Arial", size=6)  # Reduced font size for footer
        pdf.cell(190, 5, "Confidential: This payslip is meant for the named employee only. Unauthorized distribution is prohibited.", ln=True, align='C')

        payslip_file_name = f"{row['First Name ']}_{row['Second Name']}_payslip_{month}.pdf"
        pdf.output(f"/Users/elviraoredein/Desktop/payroll_generator/payslips/{payslip_file_name}")
   
    # Save as Excel
    employees.to_excel(path_to_admin_payslip_file, index=False)
    print(Fore.GREEN + "Payroll successfully generated for month " + str(month))
    # Save as CSV
    employees.to_csv(f"payslips_{month}.csv")


def report_cumulative_totals():
    employees = pd.read_excel(path_to_admin_payslip_file)

    # Sort rows by pay period to ensure we're going from Jan -> Dec
    employees.sort_values(by=['Pay Period'])

    gross_cumulatives = defaultdict(lambda: 0)
    tax_cumulatives = defaultdict(lambda: 0)
    net_cumulatives = defaultdict(lambda: 0)

    # Loop through each row
    for index, row in employees.iterrows():
        gross_cumulatives[row['Emp ID']] = round(gross_cumulatives[row['Emp ID']] + row['Gross'],2)
        employees.at[index, 'Cum (YTD) Gross'] = gross_cumulatives[row['Emp ID']]

        tax_cumulatives[row['Emp ID']] = round(tax_cumulatives[row['Emp ID']] + (row['Gross'] - row['Net Pay']),2)
        employees.at[index, 'Cum (YTD) Tax'] = tax_cumulatives[row['Emp ID']]

        net_cumulatives[row['Emp ID']] = round(net_cumulatives[row['Emp ID']] + row['Net Pay'],2)
        employees.at[index, 'Cum (YTD) Net'] = net_cumulatives[row['Emp ID']]

    employees.to_excel(path_to_admin_payslip_file, index=False)

    print(Fore.YELLOW + "\nCumulative Totals for the Year")
    print(Fore.YELLOW + "--------------------------------")

    for key, value in gross_cumulatives.items():
        print(f"Employee ID: {key} | Gross Pay: {round(value,2)} | Tax: {round(tax_cumulatives[key],2)} | Net Pay: {round(net_cumulatives[key],2)}")


def display_help():
    print(Fore.MAGENTA + "\nEnter 'a' to run the payroll for a specific month.")
    print(Fore.MAGENTA + "Enter 'b' to view the cumulative totals for the year.")
    print(Fore.MAGENTA + "Enter 'c' to add/remove employees.")
    print(Fore.MAGENTA + "Enter 'd' to display this help menu.")
    print(Fore.MAGENTA + "Enter 'e' to exit the program.")

if __name__ == "__main__":
    main()




