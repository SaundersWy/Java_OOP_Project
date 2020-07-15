# Curtis Saunders, Final Project, CIS 345, 10:30 AM
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import json
import csv
import personnel
import products
import orders
from time import ctime


def no_entry(event):
    """No Entry Allowed in Entry Widget"""
    valid_keys = ''

    if event.char not in valid_keys:
        return "break"


def num_entry(event):
    """Number Only Entry in Entry Widget"""
    valid_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\b']

    if event.char not in valid_keys:
        return "break"


def set_to_no_entry():
    """Binds widgets to the no_entry function"""
    productID_entry.bind('<Key>', no_entry)
    description_entry.bind('<Key>', no_entry)
    quantity_entry.bind('<Key>', no_entry)
    price_entry.bind('<Key>', no_entry)
    attachable_entry.bind('<Key>', no_entry)
    material_entry.bind('<Key>', no_entry)


def set_to_entry():
    """Unbinds widgets"""
    productID_entry.unbind('<Key>')
    description_entry.unbind('<Key>')
    quantity_entry.unbind('<Key>')
    price_entry.unbind('<Key>')
    attachable_entry.unbind('<Key>')
    material_entry.unbind('<Key>')


def clear_item_entries():
    """Sets variables to blank"""
    product_id_display.set('')
    description_display.set('')
    quantity_display.set('')
    price_display.set('')
    attachable_display.set('')
    material_display.set('')
    item_combobox.set('')


def update_prod_list():
    """Updates the current list of products when started"""
    global dict_of_products, product_names, list_of_products, price_of_order

    dict_of_products = dict()

    with open('products.json', 'r') as fp:
        dict_of_products = json.load(fp)
    # print(dict_of_products)

    product_names = list()
    list_of_products = list()

    for prodid in dict_of_products:
        if len(dict_of_products[prodid]) == 3:
            list_of_products.append(products.Products(prodid, dict_of_products[prodid][0],
                                                      dict_of_products[prodid][1], dict_of_products[prodid][2]))
        elif len(dict_of_products[prodid]) == 5:
            list_of_products.append(products.Attachables(prodid, dict_of_products[prodid][0],
                                                         dict_of_products[prodid][1], dict_of_products[prodid][2],
                                                         dict_of_products[prodid][3], dict_of_products[prodid][4]))
    for product in list_of_products:
        product_names.append(product.description)

    # print(product_names)
    # print(list_of_products)


def update_name_list():
    """Updates personnel when started"""
    global list_of_personnel, personnel_names, name_combo_box

    list_of_personnel = list()
    personnel_names = list()

    with open('personnel.csv', 'r') as fp:
        reader = csv.reader(fp)
        for line in reader:
            list_of_personnel.append(personnel.Personnel(line[0], line[1], line[2], line[3], line[4]))

    for people in list_of_personnel:
        personnel_names.append(people.name)


def display_item_info(event):
    """Displays Item info when item is chosen"""
    global item_combobox, product_id_display, description_display, quantity_display, price_display, \
        attachable_display, material_display, dict_of_products, list_of_products

    current_product = item_combobox.get()
    print(current_product)

    for product in list_of_products:
        if current_product in product.description:
            product_id_display.set(product.prod_id)
            description_display.set(product.description)
            quantity_display.set(product.quantity)
            price_display.set(f'${product.price}')
            if isinstance(product, products.Attachables):
                attachable_display.set(product.attach_id)
                material_display.set(product.material)
            elif isinstance(product, products.Products):
                attachable_display.set('N/A')
                material_display.set('N/A')
        print(product.description)
    quantity_of_choice.config(state=NORMAL)
    desired_quantity.set('1')


def display_name_info(event):
    """Displays info of person selected, whether they be an employee or customer"""
    global list_of_personnel, personnel_names, balance_display, account_num_display, name_combo_box, \
        list_of_products, product_names

    for people in list_of_personnel:
        if people.name == name_combo_box.get():
            balance_display.set(f'${(float(people.balance)):.2f}')
            account_num_display.set(people.acct_num)
            if people.p_type == 'C':
                customer_option.select()
                for product in list_of_products:
                    product_names.append(product.description)
                item_combobox.config(values=product_names)
                order_button.config(text='Order', command=commit_order)
                add_button.config(command=add_to_cart)
                item_combobox.config(state=NORMAL)
                item_combobox.set('Choose a Product')
                product_listbox.unbind('<Double-Button-1>')
                product_listbox.bind('<Double-Button-1>', edit_selection)
                product_listbox.bind('<Double-Button-3>', edit_selection)

                set_to_no_entry()
                clear_item_entries()

                quantity_of_choice.pack(side=RIGHT, padx=5)
                quantity_num.pack(side=RIGHT)
                add_button.config(state=NORMAL)

                if len(order_list) >= 1 and len(order_list) != len(list_of_products):
                    print('Keep Order')
                else:
                    product_listbox.delete(0, END)

            elif people.p_type == 'E':
                employee_option.select()
                order_button.config(text='Update Product', command=update_inventory)
                add_button.config(command=add_product)
                price_of_order.set('')
                set_to_entry()
                clear_item_entries()

                item_combobox.config(state=DISABLED)
                item_combobox.set('Type in Boxes for New Prod')
                product_listbox.unbind('<Double-Button-1>')
                product_listbox.unbind('<Double-Button-3>')
                product_listbox.bind('<Double-Button-1>', edit_inventory)

                product_list = list()

                desired_quantity.set('')

                quantity_of_choice.pack_forget()
                quantity_num.pack_forget()

                product_listbox.delete(0, END)

                for product in list_of_products:
                    product_listbox.insert(END, product.description)
                    print(product.description)
                    product_list.append(product)
    user_pin.config(state=NORMAL)


def add_to_cart():
    """Adds products to a cart"""
    global list_of_products, desired_quantity, item_combobox, list_of_personnel, name_combo_box, order_list, \
        product_listbox, edit_index, edit_mode, add_button, price_of_order, total_price

    current_product = item_combobox.get()

    for product in list_of_products:
        if current_product == product.description and int(product.quantity) >= int(desired_quantity.get()):
            temp_order = orders.Orders(product.description, float(desired_quantity.get()), product.price)
            quantity_display.set(int(quantity_display.get()) - int(desired_quantity.get()))
            product.quantity = quantity_display.get()
            # order_list.append(temp_order)
            # product_listbox.insert(END, temp_order)
    try:
        if edit_mode:
            order_list[edit_index] = temp_order

            product_listbox.delete(edit_index)
            product_listbox.insert(edit_index, temp_order)
            edit_mode = False
            add_button.config(text='Add')
            quantity_num.config(text='Quantity Wanted:')
        else:
            order_list.append(temp_order)
            product_listbox.insert(END, temp_order)
            # print(order_list)

        total_price = float()

        for order in order_list:
            total_price += order.total_price

        price_of_order.set(f'{total_price:.2f}')
    except (UnboundLocalError, IndexError) as ex:
        if isinstance(ex, UnboundLocalError):
            print('More than is in stock or no product chosen in the beginning.')
            messagebox.showinfo(title='Quantity Exceeds Amount', message='You have entered an amount that is too high.')
    desired_quantity.set('1')


def edit_selection(event):
    """Edit any selection made in the cart: Delete and Edit functions here"""
    """Determines if edit mode is on or off for existing student"""
    global edit_mode, edit_index, product_listbox, order_list, edit_index, list_of_products, add_button, quantity_num, \
        total_price, list_of_personnel

    # edit_mode = True
    try:
        edit_index = product_listbox.curselection()[0]
        edit_cart_selection = order_list[edit_index]

        button_clicked = event.num

        if button_clicked == 1:
            edit_mode = True
            for product in list_of_products:
                if product.description == edit_cart_selection.item:
                    item_combobox.set(product.description)
                    product_id_display.set(product.prod_id)
                    description_display.set(product.description)
                    quantity_display.set(int(product.quantity) + int(edit_cart_selection.quantity))
                    price_display.set(product.price)
                    attachable_display.set('N/A')
                    material_display.set('N/A')
                    if isinstance(product, products.Attachables):
                        attachable_display.set(product.attach_id)
                        material_display.set(product.material)
            desired_quantity.set(int(edit_cart_selection.quantity))
            add_button.config(text='Update')
            quantity_num.config(text='New Quantity:')

        delete_price = float()

        if button_clicked == 3:
            for product in list_of_products:
                if product.description == edit_cart_selection.item:
                    quantity_display.set(int(product.quantity) + int(edit_cart_selection.quantity))
                    product.quantity = int(product.quantity) + int(edit_cart_selection.quantity)
                    delete_price = order_list[edit_index].total_price
                    del order_list[edit_index]

            product_listbox.delete(edit_index)
            price_of_order.set(f'{price_of_order.get() - delete_price:.2f}')
            add_button.config(command=add_to_cart)

    except IndexError as ex:
        print('Clicked in box with no product there.')


def commit_order():
    """Commits order and tests the users balance and PIN"""
    global order_list, list_of_personnel, list_of_products, user_pin, price_of_order

    current_user = name_combo_box.get()

    for person in list_of_personnel:
        if current_user == person.name:
            if person.p_type == 'C':
                if float(person.balance) < price_of_order.get():
                    user_pin_entry.set('Low Bal')
                elif user_pin_entry.get() != person.pin:
                    user_pin_entry.set('####')
                else:
                    person.balance = str(float(person.balance) - float(price_of_order.get()))
                    product_listbox.delete(0, END)

                    order_log_add()

                    name_combo_box.set('***Choose Account***')
                    balance_display.set('$0.00')
                    account_num_display.set('-----')
                    price_of_order.set(0.00)


def edit_inventory(event):
    """Editing Inventory for Employee when item is clicked"""
    global list_of_products, choice_index, edit_inv_selection

    choice_index = product_listbox.curselection()[0]
    # print(choice_index)
    edit_inv_selection = list_of_products[choice_index]

    for product in list_of_products:
        if product.description == edit_inv_selection.description:
            if isinstance(product, products.Attachables):
                attachable_display.set(product.attach_id)
                material_display.set(product.material)
            else:
                print('normal')
                # attachable_display.set('N/A')
                # material_display.set('N/A')
            item_combobox.set(product.description)
            product_id_display.set(product.prod_id)
            description_display.set(product.description)
            quantity_display.set(product.quantity)
            price_display.set(product.price)


def update_inventory():
    """Updates all current info of any product that was chosen to be edited"""
    global list_of_products, edit_inv_selection, choice_index, list_of_personnel

    for people in list_of_personnel:
        if name_combo_box.get() == people.name:
            if people.pin == user_pin_entry.get():
                for product in list_of_products:
                    if edit_inv_selection.description == product.description:
                        if isinstance(edit_inv_selection, products.Attachables):
                            product.attach_id = attachable_display.get()
                            product.material = material_display.get()
                        product.prod_id = product_id_display.get()
                        product.description = description_display.get()
                        product.price = float(price_display.get())
                        product.quantity = int(quantity_display.get())

    clear_item_entries()
    product_listbox.delete(0, END)

    for product in list_of_products:
        product_listbox.insert(END, product.description)


def add_product():
    """New item is added to the item catalog"""
    global list_of_products, list_of_personnel

    for people in list_of_personnel:
        if name_combo_box.get() == people.name:
            if people.pin == user_pin_entry.get():
                if attachable_display.get() == '' or material_display.get() == '':
                    temp_product = products.Products(product_id_display.get(), description_display.get(),
                                                     int(quantity_display.get()), float(price_display.get()))
                else:
                    temp_product = products.Attachables(product_id_display.get(), description_display.get(),
                                                        int(quantity_display.get()), float(price_display.get()),
                                                        attachable_display.get(), material_display.get())

                list_of_products.append(temp_product)

    clear_item_entries()
    product_listbox.delete(0, END)

    for product in list_of_products:
        product_listbox.insert(END, product.description)
        print(product.description)


def order_log_add():
    """Adds a log of each order made"""
    global order_list, list_of_personnel, name_combo_box
    with open('order_log.json', 'r') as fp:
        logs = json.load(fp)

    all_orders = []

    # print(len(logs))

    if len(logs) == 1:
        for order in order_list:
            all_orders.append([order.item, int(order.quantity)])
        logs[1] = [name_combo_box.get(), all_orders, price_total.get(), ctime()]
        with open('order_log.json', 'w') as fp:
            json.dump(logs, fp)
    else:
        for order in order_list:
            all_orders.append([order.item, order.quantity])
        logs[len(logs)] = [name_combo_box.get(), all_orders, price_total.get(), ctime()]
        with open('order_log.json', 'w') as fp:
            json.dump(logs, fp)


def save_info():
    """Saves all current changes made from ordering, updating, deleting, or editing"""
    global list_of_products, list_of_personnel, dict_of_products

    updated_products = dict()
    updated_personnel = list()

    for x in list_of_products:
        if isinstance(x, products.Products):
            updated_products[x.prod_id] = [x.description, int(x.quantity), x.price]
        elif isinstance(x, products.Attachables):
            updated_products[x.prod_id] = [x.description, int(x.quantity), x.price, x.attach_id, x.material]
        # print('Saved')

    for x, y in updated_products.items():
        print(x, y)

    for x in list_of_personnel:
        updated_personnel.append([x.acct_num, x.name, x.pin, x.balance, x.p_type])

    with open('products.json', 'w') as fp:
        json.dump(updated_products, fp)

    with open('personnel.csv', 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(updated_personnel)


def open_files():
    """Prints Out Contents in each File"""

    print('***PRODUCTS IN STORE***')
    with open('products.json', 'r') as fp:
        file_products = json.load(fp)
        for prod, info in file_products.items():
            print(prod, info)

    print('\n***ALL PERSONNEL***')
    with open('personnel.csv', 'r') as fp:
        reader = csv.reader(fp)
        for line in reader:
            print(line)

    print('\n***ORDER LOGS***')
    with open('order_log.json', 'r') as fp:
        past_orders = json.load(fp)
        for log_num, log_info in past_orders.items():
            print(log_num, log_info)
    print('\n')


update_name_list()
update_prod_list()

''' TKINTER CONSTRUCTION OF APPLICATION'''
win = Tk()
win.geometry('715x412')
win.config(bg='light blue')
win.title('KITCHEN SUPPLY')
win.resizable(0, 0)
win.iconbitmap('bit_icon.ico')
text_type = 'Times'
textsize = 10
background = 'cornsilk'

# Variables
edit_mode = False
edit_index = int()
order_list = []

# Text Variables
product_id_display = StringVar()
description_display = StringVar()
quantity_display = StringVar()
price_display = StringVar()
attachable_display = StringVar()
material_display = StringVar()
price_of_order = DoubleVar()
desired_quantity = StringVar()
user_pin_entry = StringVar()
account_num_display = StringVar()
balance_display = StringVar()

# Menu Bar
menu_bar = Menu(win)
win.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=False, border=2)
menu_bar.add_cascade(label='Options', menu=file_menu)
file_menu.add_command(label='Open Files', command=open_files)
file_menu.add_command(label='Save', command=save_info)
file_menu.add_command(label='Exit', command=win.quit)

'''FRAMES FOR APP LAYOUT'''
# Logo
logo_frame = Frame(win, bg='pink', height=100, width=250, relief=GROOVE, bd=2)
logo_frame.grid(row=0, column=0, rowspan=1, sticky=NSEW)

filename = 'logo.png'
logo = ImageTk.PhotoImage(Image.open(filename))
logo_in_frame = Label(logo_frame, image=logo)
logo_in_frame.pack(side=LEFT)

Label(logo_frame, text='Kitchen\n  Supply', width=11, font=('ms serif', 24), bg='pink', justify=LEFT).pack(side=LEFT)

# Customer/Employee, Name Drop, Acct Edit Fields
account_info = Frame(win, bg='orange', relief=SUNKEN, height=100, width=350)
account_info.grid(row=0, column=1, rowspan=2, sticky=NSEW)

empty_space = Label(account_info, bg='orange', width=20, height=3).grid(row=0, column=0, columnspan=1)

name_combo_box = ttk.Combobox(account_info, values=personnel_names, font=(text_type, textsize), width=27)
name_combo_box.grid(row=0, column=2, columnspan=2, sticky=E)
name_combo_box.bind('<<ComboboxSelected>>', display_name_info)
name_combo_box.bind('<Key>', no_entry)
name_combo_box.set('***Choose Account***')

employee_option = Radiobutton(account_info, bg=background, text='Employee', value='E',
                              height=1, width=10, font=(text_type, textsize), state=DISABLED, relief=SUNKEN)
employee_option.grid(row=1, column=0, sticky=W, padx=5)
customer_option = Radiobutton(account_info, bg=background, text='Customer', value='C',
                              height=1, width=10, font=(text_type, textsize), state=DISABLED, relief=SUNKEN)
customer_option.grid(row=2, column=0, sticky=W, padx=5)

Label(account_info, text='Acct #:', justify=RIGHT, font=(text_type, textsize), bg=background,
      relief=RAISED).grid(row=1, column=2, sticky=E, padx=5, pady=5)
Label(account_info, text='Balance:', justify=RIGHT, font=(text_type, textsize), bg=background,
      relief=RAISED).grid(row=2, column=2, sticky=E, padx=5, pady=5)

account_num_entry = Entry(account_info, font=(text_type, textsize), textvariable=account_num_display)
account_num_entry.grid(row=1, column=3, columnspan=2, sticky=E)
account_num_entry.bind('<Key>', no_entry)
account_num_display.set('-----')

balance_entry = Entry(account_info, font=(text_type, textsize), textvariable=balance_display)
balance_entry.grid(row=2, column=3, columnspan=2, sticky=E)
balance_entry.bind('<Key>', no_entry)
balance_display.set('$0.00')

# Item DropDown for Customers, Item Creation for employees
item_selection_frame = Frame(win, bg=background, bd=4, relief=GROOVE, height=350, width=350)
item_selection_frame.grid(row=1, column=0, rowspan=6, sticky=NSEW)

empty1 = Label(item_selection_frame, bg=background, width=6).grid(row=0, column=0)

item_combobox = ttk.Combobox(item_selection_frame, values=product_names, font=(text_type, textsize), width=27)
item_combobox.grid(row=0, column=2, columnspan=2, padx=2)
item_combobox.bind('<<ComboboxSelected>>', display_item_info)
item_combobox.bind('<Key>', no_entry)

Label(item_selection_frame, text='Product ID:', bg=background, relief=RAISED,
      font=(text_type, textsize)).grid(row=1, column=1, pady=5, sticky=E)
Label(item_selection_frame, text='Description:', bg=background, relief=RAISED,
      font=(text_type, textsize)).grid(row=2, column=1, pady=3, sticky=E)
Label(item_selection_frame, text='Quantity:', bg=background, relief=RAISED,
      font=(text_type, textsize)).grid(row=3, column=1, pady=3, sticky=E)
Label(item_selection_frame, text='Price:', bg=background, relief=RAISED,
      font=(text_type, textsize)).grid(row=4, column=1, pady=3, sticky=E)
Label(item_selection_frame, text='Attachable PID:', bg=background, relief=RAISED,
      font=(text_type, textsize)).grid(row=5, column=1, pady=3, sticky=E)
Label(item_selection_frame, text='Material Type:', bg=background, relief=RAISED,
      font=(text_type, textsize)).grid(row=6, column=1, pady=3, sticky=E)

productID_entry = Entry(item_selection_frame, font=(text_type, textsize), width=25, textvariable=product_id_display)
productID_entry.grid(row=1, column=2)
productID_entry.bind('<Key>', no_entry)

description_entry = Entry(item_selection_frame, font=(text_type, textsize), width=25, textvariable=description_display)
description_entry.grid(row=2, column=2)
description_entry.bind('<Key>', no_entry)

quantity_entry = Entry(item_selection_frame, font=(text_type, textsize), width=25, textvariable=quantity_display)
quantity_entry.grid(row=3, column=2)
quantity_entry.bind('<Key>', no_entry)

price_entry = Entry(item_selection_frame, font=(text_type, textsize), width=25, textvariable=price_display)
price_entry.grid(row=4, column=2)
price_entry.bind('<Key>', no_entry)

attachable_entry = Entry(item_selection_frame, font=(text_type, textsize), width=25, textvariable=attachable_display)
attachable_entry.grid(row=5, column=2)
attachable_entry.bind('<Key>', no_entry)

material_entry = Entry(item_selection_frame, font=(text_type, textsize), width=25, textvariable=material_display)
material_entry.grid(row=6, column=2)
material_entry.bind('<Key>', no_entry)

# Display of Items in List Box
items_list = Frame(win, bg=background, bd=5, relief=GROOVE, height=200, width=250)
items_list.grid(row=2, column=1, rowspan=5, sticky=NSEW)

Label(items_list, text='Current Order', font=(text_type, 14), bg=background, relief=RAISED).pack(pady=5)

product_listbox = Listbox(items_list, width=60)
product_listbox.pack(fill=BOTH)

price_total = Entry(items_list, width=15, justify=RIGHT, textvariable=price_of_order)
price_total.pack(side=RIGHT, anchor=S)
price_total.bind('<Key>', no_entry)

total_label = Label(items_list, text='Total: $', bg=background, relief=RAISED)
total_label.pack(side=RIGHT, anchor=S, padx=5)

# Desired Quantity + Add Button for List and New Product
add_field = Frame(win, height=50, width=250, bg='light gray', relief=SUNKEN)
add_field.grid(row=7, column=0, rowspan=2, sticky=NSEW)

add_button = Button(add_field, text='ADD', command=add_to_cart, bg=background, relief=RAISED)
add_button.pack(side=RIGHT, padx=15)

quantity_of_choice = Entry(add_field, width=5, textvariable=desired_quantity, state=DISABLED)
quantity_of_choice.pack(side=RIGHT, padx=5)
quantity_of_choice.bind('<Key>', num_entry)

quantity_num = Label(add_field, text='Quantity Wanted:', bg=background, relief=RIDGE)
quantity_num.pack(side=RIGHT)

# Order Button + Pin Entry
order_pin_field = Frame(win, height=100, width=350, bg='light gray', relief=SUNKEN)
order_pin_field.grid(row=7, column=1, rowspan=1, sticky=NSEW)

order_button = Button(order_pin_field, text='Order', bg=background, relief=RAISED)
order_button.pack(side=RIGHT, padx=5)

user_pin = Entry(order_pin_field, width=7, textvariable=user_pin_entry, state=DISABLED)
user_pin.pack(side=RIGHT, padx=5)
user_pin.bind('<Key>', num_entry)

Label(order_pin_field, text='Pin:', bg=background, relief=RIDGE).pack(side=RIGHT, padx=5)

product_id_display.set('(Product ID)')
description_display.set('(Product Name')
quantity_display.set('(Quantity in Stock')
price_display.set('(Price of Product')
attachable_display.set('(Attachable Prod ID)')
material_display.set('(Material of Attachable)')
item_combobox.set('(Choose a Product)')
desired_quantity.set('1')

win.mainloop()
