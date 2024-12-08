from tkinter import *
from tkinter import ttk,messagebox
import ttkbootstrap as tb
import sqlite3 


    
#================================================
#============ VENTANAS PRINCIPALes ==============
#================================================
class Ventana(tb.Window):
    def __init__(self):
        super().__init__()
        self.ventana_login()
  
    # Método para crear la ventana de inicio de sesión
    def ventana_login(self):
        self.frame_login = Frame(self)
        self.frame_login.pack()

        self.lblframe_login = LabelFrame(self.frame_login, text='Acceso')
        self.lblframe_login.pack(padx=10, pady=10)

        lbltitulo = Label(self.lblframe_login, text='Inicio de sesion',font=('Arial',18))
        lbltitulo.pack(padx=10, pady=35)

        self.txt_usuario = ttk.Entry(self.lblframe_login,width=40,justify=CENTER)  # Campo para el nombre de usuario
        self.txt_usuario.pack(padx=10, pady=10)
        
        self.txt_clave = ttk.Entry(self.lblframe_login,width=40,justify=CENTER)  # Campo para la contraseña
        self.txt_clave.pack(padx=10, pady=10)
        self.txt_clave.configure(show='*')  # Oculta la contraseña

        btn_acceso = ttk.Button(self.lblframe_login, text='Log in',width=38,command=self.logueo)  # Botón para iniciar sesión
        btn_acceso.pack(padx=10, pady=10)

    # Método para crear la ventana del menú
    def ventana_menu(self):
        self.frame_left=Frame(self,width=200)
        self.frame_left.grid(row=0,column=0,sticky=NS)
        
        self.frame_center=Frame(self)
        self.frame_center.grid(row=0,column=1,sticky=NSEW)
        
        self.frame_right=Frame(self,width=400)
        self.frame_right.grid(row=0,column=2,sticky=NSEW)

        # Botones del menú
        btn_productos=ttk.Button(self.frame_left,text='Productos',width=15,command=self.ventana_lista_productos)
        btn_productos.grid(row=0,column=0,padx=10,pady=10)

        btn_ventas=ttk.Button(self.frame_left,text='Ventas',width=15,command=self.ventana_lista_ventas)
        btn_ventas.grid(row=1,column=0,padx=10,pady=10)

        btn_clientes=ttk.Button(self.frame_left,text='Clientes',width=15,command=self.ventana_lista_clientes)
        btn_clientes.grid(row=2,column=0,padx=10,pady=10)

        btn_compras=ttk.Button(self.frame_left,text='Compras',width=15,command=self.ventana_lista_compras)
        btn_compras.grid(row=3,column=0,padx=10,pady=10)

        btn_usuarios=ttk.Button(self.frame_left,text='Usuarios',width=15,command=self.ventana_lista_usuarios)
        btn_usuarios.grid(row=4,column=0,padx=10,pady=10)

        btn_reportes=ttk.Button(self.frame_left,text='Reportes',width=15,command=self.ventana_lista_reportes)
        btn_reportes.grid(row=5,column=0,padx=10,pady=10)

        lbl2=Label(self.frame_center,text='')
        lbl2.grid(row=0,column=0,padx=10,pady=10)

        lbl3=Label(self.frame_right,text='')
        lbl3.grid(row=0,column=0,padx=10,pady=10)

    # Método para el proceso de inicio de sesión
    def logueo(self):

        try:
            # Establecer la conexión a la base de datos 
            miConexion=sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor=miConexion.cursor()
            
            nombre_usuario=self.txt_usuario.get()
            clave_usuario=self.txt_clave.get()

            # Consultar la base de datos 
            miCursor.execute("SELECT * FROM Usuarios WHERE Nombre=? AND Clave=?",(nombre_usuario,clave_usuario))
            # Obtener los registros
            datos_logeo=miCursor.fetchall()
            if datos_logeo!="":
                for row in datos_logeo:
                    cod_usu=row[0]
                    nom_usu=row[1]
                    cla_usu=row[2]
                    rol_usu=row[3]
                if(nom_usu==self.txt_usuario.get() and cla_usu==self.txt_clave.get()):         
                    self.frame_login.pack_forget()  # Ocultar la ventana de inicio de sesión
                    self.ventana_menu()  # Mostrar la ventana del menú 
            
            # Aplicar cambios 
            miConexion.commit()
            # Cerrar la conexión 
            miConexion.close()
        
        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Acceso", "El usuario o clave son incorrectos")

#====================================
#============ Usuarios ==============
#====================================
    def ventana_lista_usuarios(self):

        self.frame_lista_usuarios=Frame(self.frame_center)
        self.frame_lista_usuarios.grid(row=0,column=0,columnspan=2,sticky=NSEW)

        self.lblframe_botones_listusu=LabelFrame(self.frame_lista_usuarios)
        self.lblframe_botones_listusu.grid(row=0,column=0,padx=10,pady=10,sticky=NSEW)

        btn_nuevo_usuario=tb.Button(self.lblframe_botones_listusu,text='Nuevo',width=15
                                    ,bootstyle="success",command=self.ventana_nuevo_usuario)
        btn_nuevo_usuario.grid(row=0,column=0,padx=5,pady=5)

        btn_modificar_usuario=tb.Button(self.lblframe_botones_listusu,text='Modificar',width=15,bootstyle="warning",command=self.ventana_modificar_usuario)
        btn_modificar_usuario.grid(row=0,column=1,padx=5,pady=5)
        
        btn_eliminar_usuario=tb.Button(self.lblframe_botones_listusu,text='Eliminar',width=15,bootstyle="danger",command=self.ventana_eliminar_usuario)
        btn_eliminar_usuario.grid(row=0,column=2,padx=5,pady=5)


        self.lblframe_busqueda_listusu=LabelFrame(self.frame_lista_usuarios)
        self.lblframe_busqueda_listusu.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)

        self.txt_busqueda_usuarios=ttk.Entry(self.lblframe_busqueda_listusu,width=73)
        self.txt_busqueda_usuarios.grid(row=0,column=0,padx=5,pady=5)
        self.txt_busqueda_usuarios.bind('<Key>',self.buscar_usuario)


        self.lblframe_tree_listusu=LabelFrame(self.frame_lista_usuarios)
        self.lblframe_tree_listusu.grid(row=2,column=0,padx=10,pady=10,sticky=NSEW)

        columnas=("codigo","nombre","clave","rol")

        self.tree_lista_usuarios=tb.Treeview(self.lblframe_tree_listusu,columns=columnas,
                                        height=17,show='headings',bootstyle='dark')
        self.tree_lista_usuarios.grid(row=0,column=0)

        self.tree_lista_usuarios.heading("codigo",text="Codigo",anchor=W)
        self.tree_lista_usuarios.heading("nombre",text="Nombre",anchor=W)
        self.tree_lista_usuarios.heading("clave",text="Clave",anchor=W)
        self.tree_lista_usuarios.heading("rol",text="Rol",anchor=W)
        self.tree_lista_usuarios['displaycolumns']=("codigo","nombre","rol")

        #crear el scrolbar
        tree_scroll_listausu=tb.Scrollbar(self.frame_lista_usuarios,bootstyle="round-success")
        tree_scroll_listausu.grid(row=2,column=1)
        
        #configurar el scrolbar
        tree_scroll_listausu.config(command=self.tree_lista_usuarios.yview)

        #Llamamos a nuestra funcion mostrar usuarios 
        self.mostrar_usuarios()

    def mostrar_usuarios(self):
        try:
            #establecer la coneccion 
            miConexion=sqlite3.connect('Sispuntoventas.db')
            #creamos el cursor
            miCursor=miConexion.cursor()
            #limpiamos nuestro treeview
            registros=self.tree_lista_usuarios.get_children()
            #recorremos cada registro
            for elementos in registros:
                self.tree_lista_usuarios.delete(elementos)
            #consultamos nuestra base de datos 
            miCursor.execute("SELECT * FROM Usuarios")
            #con esto tendremos todos los registros y lo guardamos en "datos"
            datos=miCursor.fetchall()
            #recorremos cada fila encontrada 
            for row in datos:
                #llenamos nuestro treeview
                self.tree_lista_usuarios.insert("",0,text=row[0],values=(row[0],row[1],row[2],row[3]))
            #aplicamos cambios 
            miConexion.commit()
            #cerramos la conexion 
            miConexion.close()
        
        
        except:
            messagebox.showerror("Lista de Usuario", "Ocurrió un error al mostrar la lista de usuarios")

    def ventana_nuevo_usuario(self):

        self.frame_nuevo_usuario=Toplevel(self)
        self.frame_nuevo_usuario.title('Nuevo Usuario')
        self.frame_nuevo_usuario.geometry('470x470')
        self.frame_nuevo_usuario.resizable(0,0)
        self.frame_nuevo_usuario.grab_set()

        lblframe_nuevo_usuario=LabelFrame(self.frame_nuevo_usuario)
        lblframe_nuevo_usuario.grid(row=0,column=0,sticky=NSEW,padx=10,pady=10)

        lbl_codigo_nuevo_usuario=Label(lblframe_nuevo_usuario,text='Codigo')
        lbl_codigo_nuevo_usuario.grid(row=0,column=0,padx=10,pady=10)
        self.txt_codigo_nuevo_usuario=Entry(lblframe_nuevo_usuario,width=40)
        self.txt_codigo_nuevo_usuario.grid(row=0,column=1,padx=10,pady=10)

        
        lbl_nombre_nuevo_usuario=Label(lblframe_nuevo_usuario,text='Nombre')
        lbl_nombre_nuevo_usuario.grid(row=1,column=0,padx=10,pady=10)
        self.txt_nombre_nuevo_usuario=Entry(lblframe_nuevo_usuario,width=40)
        self.txt_nombre_nuevo_usuario.grid(row=1,column=1,padx=10,pady=10)

        
        lbl_clave_nuevo_usuario=Label(lblframe_nuevo_usuario,text='Clave')
        lbl_clave_nuevo_usuario.grid(row=2,column=0,padx=10,pady=10)
        self.txt_clave_nuevo_usuario=Entry(lblframe_nuevo_usuario,width=40)
        self.txt_clave_nuevo_usuario.grid(row=2,column=1,padx=10,pady=10)

        
        lbl_rol_nuevo_usuario=Label(lblframe_nuevo_usuario,text='Rol')
        lbl_rol_nuevo_usuario.grid(row=3,column=0,padx=10,pady=10)
        self.txt_rol_nuevo_usuario=ttk.Combobox(lblframe_nuevo_usuario,values=('Administrador','Almacen','Vendedor'),width=40,state='readonly')
        self.txt_rol_nuevo_usuario.grid(row=3,column=1,padx=10,pady=10)
        self.txt_rol_nuevo_usuario.current()

        btn_guardar_nuevo_usuario=ttk.Button(lblframe_nuevo_usuario,text='Guardar',width=38,command=self.guardar_usuario)
        btn_guardar_nuevo_usuario.grid(row=4,column=1,padx=10,pady=10)

        #llamamos a la funcion ultimo usuario
        self.ultimo_usuario()

    def guardar_usuario(self):
        #validamos para que no queden vacios los campos 
        if self.txt_codigo_nuevo_usuario.get() == "" or self.txt_nombre_nuevo_usuario.get() == "" or self.txt_clave_nuevo_usuario.get() == "":
                messagebox.showwarning("Guardando Usuarios", "Por favor, complete todos los campos para guardar un nuevo usuario.")
                return

        try:
            #establecer la coneccion 
            miConexion=sqlite3.connect('Sispuntoventas.db')
            #creamos el cursor
            miCursor=miConexion.cursor()

            datos_guardar_usuario = (
            self.txt_codigo_nuevo_usuario.get(),
            self.txt_nombre_nuevo_usuario.get(),
            self.txt_clave_nuevo_usuario.get(),
            self.txt_rol_nuevo_usuario.get()
        )
        
            #consultamos nuestra base de datos 
            miCursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?)",(datos_guardar_usuario))
            messagebox.showinfo('Guardando Usuarios',"Usuario Guardado Correctamente")
            #aplicamos cambios 
            miConexion.commit()
            self.frame_nuevo_usuario.destroy()#cerramos la ventana 
            self.ventana_lista_usuarios()#cargamos la ventana para ver los cambios 
            #cerramos la conexion 
            miConexion.close()
        
        
        except:
            messagebox.showerror("Guardando Usuario","Ocurrio un error al Guardar Usuario")

    def ultimo_usuario(self):
        try:
            #establecer la coneccion 
            miConexion=sqlite3.connect('Sispuntoventas.db')
            #creamos el cursor
            miCursor=miConexion.cursor()
           
            #consultamos nuestra base de datos 
            miCursor.execute("SELECT MAX(Codigo) FROM Usuarios")
            #con esto tendremos todos los registros y lo guardamos en "datos"
            datos=miCursor.fetchone()#solo necesitamos un dato 
            for codusu in datos:
                if codusu==None:
                    self.ultusu=(int(1))
                    self.txt_codigo_nuevo_usuario.configure(state=NORMAL)
                    self.txt_codigo_nuevo_usuario.insert(0,self.ultusu)
                    self.txt_codigo_nuevo_usuario.configure(state='readonly')
                    break
                if codusu=="":
                    self.ultusu=(int(1))
                    self.txt_codigo_nuevo_usuario.configure(state=NORMAL)
                    self.txt_codigo_nuevo_usuario.insert(0,self.ultusu)
                    self.txt_codigo_nuevo_usuario.configure(state='readonly')
                    break

                else:
                    self.ultusu=(int(codusu)+1)
                    self.txt_codigo_nuevo_usuario.configure(state=NORMAL)
                    self.txt_codigo_nuevo_usuario.insert(0,self.ultusu)
                    self.txt_codigo_nuevo_usuario.configure(state='readonly')
            
            #aplicamos cambios 
            miConexion.commit()
            #cerramos la conexion 
            miConexion.close()
        
        
        except:
            messagebox.showerror("Nuevo Usuario", "Ocurrió un error al mostrar la ventana Nuevo Usuario")

    def buscar_usuario(self,event):
        try:
            #establecer la coneccion 
            miConexion=sqlite3.connect('Sispuntoventas.db')
            #creamos el cursor
            miCursor=miConexion.cursor()
            #limpiamos nuestro treeview
            registros=self.tree_lista_usuarios.get_children()
            #recorremos cada registro
            for elementos in registros:
                self.tree_lista_usuarios.delete(elementos)
            #consultamos nuestra base de datos 
            miCursor.execute("SELECT * FROM Usuarios WHERE Nombre LIKE ?",(self.txt_busqueda_usuarios.get()
            +'%',))
            #con esto tendremos todos los registros y lo guardamos en "datos"
            datos=miCursor.fetchall()
            #recorremos cada fila encontrada 
            for row in datos:
                #llenamos nuestro treeview
                self.tree_lista_usuarios.insert("",0,text=row[0],values=(row[0],row[1],row[2],row[3]))
            #aplicamos cambios 
            miConexion.commit()
            #cerramos la conexion 
            miConexion.close()
        
        
        except:
            messagebox.showerror("Busqueda de Usuarios", "Ocurrió un error al buscar la lista de usuarios")

    def ventana_modificar_usuario(self):
        #con esto estamos validando que se abra la ventana solamente si hay algo seleccionado 
        self.usuario_seleccionado=self.tree_lista_usuarios.focus()

        self.val_mod_usu=self.tree_lista_usuarios.item(self.usuario_seleccionado,'values')

        if self.val_mod_usu!='':
            self.frame_modificar_usuario = Toplevel(self)
            self.frame_modificar_usuario.title('Modificar Usuario')
            self.frame_modificar_usuario.geometry('480x300')
            self.frame_modificar_usuario.resizable(0, 0)
            self.frame_modificar_usuario.grab_set()

            lblframe_modificar_usuario = LabelFrame(self.frame_modificar_usuario)
            lblframe_modificar_usuario.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

            lbl_codigo_modificar_usuario = Label(lblframe_modificar_usuario, text='Codigo')
            lbl_codigo_modificar_usuario.grid(row=0, column=0, padx=10, pady=10)
            self.txt_codigo_modificar_usuario = Entry(lblframe_modificar_usuario, width=40)
            self.txt_codigo_modificar_usuario.grid(row=0, column=1, padx=10, pady=10)

            lbl_nombre_modificar_usuario = Label(lblframe_modificar_usuario, text='Nombre')
            lbl_nombre_modificar_usuario.grid(row=1, column=0, padx=10, pady=10)
            self.txt_nombre_modificar_usuario = Entry(lblframe_modificar_usuario, width=40)
            self.txt_nombre_modificar_usuario.grid(row=1, column=1, padx=10, pady=10)

            lbl_clave_modificar_usuario = Label(lblframe_modificar_usuario, text='Clave')
            lbl_clave_modificar_usuario.grid(row=2, column=0, padx=10, pady=10)
            self.txt_clave_modificar_usuario = Entry(lblframe_modificar_usuario, width=40)
            self.txt_clave_modificar_usuario.grid(row=2, column=1, padx=10, pady=10)

            lbl_rol_modificar_usuario = Label(lblframe_modificar_usuario, text='Rol')
            lbl_rol_modificar_usuario.grid(row=3, column=0, padx=10, pady=10)
            self.txt_rol_modificar_usuario = ttk.Combobox(lblframe_modificar_usuario, values=('Administrador', 'Almacen', 'Vendedor'), width=40)
            self.txt_rol_modificar_usuario.grid(row=3, column=1, padx=10, pady=10)
            

            btn_guardar_modificar_usuario = ttk.Button(lblframe_modificar_usuario, text='Modificar', width=38,
            bootstyle='warning',command=self.modificar_usuario)
            btn_guardar_modificar_usuario.grid(row=4, column=1, padx=10, pady=10)
            self.llenar_entrys_modificar_usuario()

            # Llamamos a la función cargar_datos_usuario para cargar los datos del usuario a modificar
            self.txt_nombre_modificar_usuario.focus()

    def llenar_entrys_modificar_usuario(self):
        #limpiaremos todos los entrys
        self.txt_codigo_modificar_usuario.delete(0,END)
        self.txt_nombre_modificar_usuario.delete(0,END)
        self.txt_clave_modificar_usuario.delete(0,END)
        self.txt_rol_modificar_usuario.delete(0,END)

        #llenamos los entrys 
        self.txt_codigo_modificar_usuario.insert(0,self.val_mod_usu[0])
        self.txt_codigo_modificar_usuario.config(state='readonly')
        self.txt_nombre_modificar_usuario.insert(0,self.val_mod_usu[1])
        self.txt_clave_modificar_usuario.insert(0,self.val_mod_usu[2])
        self.txt_rol_modificar_usuario.insert(0,self.val_mod_usu[3])
        self.txt_rol_modificar_usuario.config(state='readonly')

    def modificar_usuario(self):
        #validamos para que no queden vacios los campos 
        if self.txt_codigo_modificar_usuario.get() == "" or self.txt_nombre_modificar_usuario.get() == "" or self.txt_clave_modificar_usuario.get() == "":
                messagebox.showwarning("Modificar Usuarios", "Por favor, complete todos los campos para guardar un nuevo usuario.")
                return

        try:
            #establecer la coneccion 
            miConexion=sqlite3.connect('Sispuntoventas.db')
            #creamos el cursor
            miCursor=miConexion.cursor()

            datos_modificar_usuario = (
            self.txt_nombre_modificar_usuario.get(),
            self.txt_clave_modificar_usuario.get(),
            self.txt_rol_modificar_usuario.get()
        )
        
            #consultamos nuestra base de datos 
            miCursor.execute("UPDATE Usuarios SET Nombre=?,Clave=?,Rol=? WHERE Codigo="+self.txt_codigo_modificar_usuario.get()
                             ,(datos_modificar_usuario))
            messagebox.showinfo('Modificar Usuarios',"Usuario Modificado Correctamente")
            #aplicamos cambios 
            miConexion.commit()
            self.val_mod_usu=self.tree_lista_usuarios.item(self.usuario_seleccionado,text='',values=
            (self.txt_codigo_modificar_usuario.get(),self.txt_nombre_modificar_usuario.get(),
            self.txt_clave_modificar_usuario.get(),self.txt_rol_modificar_usuario.get()))
            self.frame_modificar_usuario.destroy()#cerramos la ventana 
            #cerramos la conexion 
            miConexion.close()
        
        
        except:
            messagebox.showerror("Modificar Usuario","Ocurrio un error al Modificar Usuario")

    def ventana_eliminar_usuario(self):
        # Validar que se haya seleccionado un usuario
        self.usuario_seleccionado = self.tree_lista_usuarios.focus()
        self.val_elim_usu = self.tree_lista_usuarios.item(self.usuario_seleccionado, 'values')

        if self.val_elim_usu != '':
            self.frame_eliminar_usuario = Toplevel(self)
            self.frame_eliminar_usuario.title('Eliminar Usuario')
            self.frame_eliminar_usuario.geometry('460x250')
            self.frame_eliminar_usuario.resizable(0, 0)
            self.frame_eliminar_usuario.grab_set()

            lblframe_eliminar_usuario = LabelFrame(self.frame_eliminar_usuario)
            lblframe_eliminar_usuario.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

            lbl_confirmacion = Label(lblframe_eliminar_usuario, text='¿Está seguro que desea eliminar este usuario?')
            lbl_confirmacion.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            lbl_nombre_usuario = Label(lblframe_eliminar_usuario, text='Nombre:')
            lbl_nombre_usuario.grid(row=1, column=0, padx=10, pady=10)
            lbl_nombre_usuario_valor = Label(lblframe_eliminar_usuario, text=self.val_elim_usu[1])
            lbl_nombre_usuario_valor.grid(row=1, column=1, padx=10, pady=10)

            lbl_clave_usuario = Label(lblframe_eliminar_usuario, text='Clave:')
            lbl_clave_usuario.grid(row=2, column=0, padx=10, pady=10)
            lbl_clave_usuario_valor = Label(lblframe_eliminar_usuario, text='*******')  # Puedes mostrar asteriscos para la clave
            lbl_clave_usuario_valor.grid(row=2, column=1, padx=10, pady=10)

            btn_eliminar_usuario = ttk.Button(lblframe_eliminar_usuario, text='Eliminar', width=38,
                                            style='danger', command=self.eliminar_usuario)
            btn_eliminar_usuario.grid(row=3, column=1, padx=10, pady=10)

    def eliminar_usuario(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Obtener el código del usuario a eliminar
            codigo_usuario = self.val_elim_usu[0]

            # Consultar la base de datos para eliminar el usuario
            miCursor.execute("DELETE FROM Usuarios WHERE Codigo=?", (codigo_usuario,))
            messagebox.showinfo('Eliminar Usuario', 'Usuario Eliminado Correctamente')
            # Aplicar cambios
            miConexion.commit()
            # Actualizar la vista de la lista de usuarios
            self.tree_lista_usuarios.delete(self.usuario_seleccionado)
            self.frame_eliminar_usuario.destroy()  # Cerrar la ventana de eliminación
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror('Eliminar Usuario', 'Ocurrió un error al eliminar el usuario')


#=====================================
#============ PRODUCTOS ==============
#=====================================
    def ventana_lista_productos(self):
        self.frame_lista_productos = Frame(self.frame_center)
        self.frame_lista_productos.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.lblframe_botones_listprod = LabelFrame(self.frame_lista_productos)
        self.lblframe_botones_listprod.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        btn_nuevo_producto = tb.Button(self.lblframe_botones_listprod, text='Nuevo', width=15, bootstyle="success",command=self.ventana_nuevo_producto)
        btn_nuevo_producto.grid(row=0, column=0, padx=5, pady=5)

        btn_modificar_producto = tb.Button(self.lblframe_botones_listprod, text='Modificar', width=15, bootstyle="warning",command=self.ventana_modificar_producto)
        btn_modificar_producto.grid(row=0, column=1, padx=5, pady=5)

        btn_eliminar_producto = tb.Button(self.lblframe_botones_listprod, text='Eliminar', width=15, bootstyle="danger",command=self.ventana_eliminar_producto)
        btn_eliminar_producto.grid(row=0, column=2, padx=5, pady=5)

        self.lblframe_busqueda_listprod = LabelFrame(self.frame_lista_productos)
        self.lblframe_busqueda_listprod.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        self.txt_busqueda_productos = ttk.Entry(self.lblframe_busqueda_listprod, width=73)
        self.txt_busqueda_productos.grid(row=0, column=0, padx=5, pady=5)
        self.txt_busqueda_productos.bind('<Key>',self.buscar_productos)

        self.lblframe_tree_listprod = LabelFrame(self.frame_lista_productos)
        self.lblframe_tree_listprod.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        columnas = ("codigo", "nombre", "precio", "stock")

        self.tree_lista_productos = tb.Treeview(self.lblframe_tree_listprod, columns=columnas,
                                             height=17, show='headings', bootstyle='dark')
        self.tree_lista_productos.grid(row=0, column=0)

        self.tree_lista_productos.heading("codigo", text="Codigo", anchor=W)
        self.tree_lista_productos.heading("nombre", text="Nombre", anchor=W)
        self.tree_lista_productos.heading("precio", text="Precio", anchor=W)
        self.tree_lista_productos.heading("stock", text="Stock", anchor=W)
        self.tree_lista_productos['displaycolumns'] = ("codigo", "nombre", "precio", "stock")

        # crear el scrollbar
        tree_scroll_listprod = tb.Scrollbar(self.frame_lista_productos, bootstyle="round-success")
        tree_scroll_listprod.grid(row=2, column=1)

        # configurar el scrollbar
        tree_scroll_listprod.config(command=self.tree_lista_productos.yview)

        #Llamamos a nuestra funcion mostrar productos
        self.mostrar_productos()

    def mostrar_productos(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()
            # Limpiar el treeview de productos
            registros = self.tree_lista_productos.get_children()
            for elemento in registros:
                self.tree_lista_productos.delete(elemento)
            # Consultar la base de datos para obtener los productos
            miCursor.execute("SELECT * FROM Productos")
            # Obtener los registros y guardarlos en "datos"
            datos = miCursor.fetchall()
            # Recorrer cada fila encontrada
            for row in datos:
                # Llenar el treeview con los datos de los productos
                self.tree_lista_productos.insert("", 0, text=row[0], values=(row[0], row[1], row[2], row[3]))
            # Aplicar cambios en la interfaz
            miConexion.commit()
            # Cerrar la conexión
            miConexion.close()
    
        except:
            messagebox.showerror("Lista de Productos", "Ocurrió un error al mostrar la lista de productos")

    def ventana_nuevo_producto(self):
        self.frame_nuevo_producto = Toplevel(self)
        self.frame_nuevo_producto.title('Nuevo Producto')
        self.frame_nuevo_producto.geometry('470x470')
        self.frame_nuevo_producto.resizable(0, 0)
        self.frame_nuevo_producto.grab_set()

        lblframe_nuevo_producto = LabelFrame(self.frame_nuevo_producto)
        lblframe_nuevo_producto.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        lbl_codigo_nuevo_producto = Label(lblframe_nuevo_producto, text='Código')
        lbl_codigo_nuevo_producto.grid(row=0, column=0, padx=10, pady=10)
        self.txt_codigo_nuevo_producto = Entry(lblframe_nuevo_producto, width=40)
        self.txt_codigo_nuevo_producto.grid(row=0, column=1, padx=10, pady=10)

        lbl_nombre_nuevo_producto = Label(lblframe_nuevo_producto, text='Nombre')
        lbl_nombre_nuevo_producto.grid(row=1, column=0, padx=10, pady=10)
        self.txt_nombre_nuevo_producto = Entry(lblframe_nuevo_producto, width=40)
        self.txt_nombre_nuevo_producto.grid(row=1, column=1, padx=10, pady=10)

        lbl_precio_nuevo_producto = Label(lblframe_nuevo_producto, text='Precio')
        lbl_precio_nuevo_producto.grid(row=2, column=0, padx=10, pady=10)
        self.txt_precio_nuevo_producto = Entry(lblframe_nuevo_producto, width=40)
        self.txt_precio_nuevo_producto.grid(row=2, column=1, padx=10, pady=10)

        lbl_stock_nuevo_producto = Label(lblframe_nuevo_producto, text='Stock')
        lbl_stock_nuevo_producto.grid(row=3, column=0, padx=10, pady=10)
        self.txt_stock_nuevo_producto = Entry(lblframe_nuevo_producto, width=40)
        self.txt_stock_nuevo_producto.grid(row=3, column=1, padx=10, pady=10)

        btn_nuevo_producto = ttk.Button(lblframe_nuevo_producto, text='Guardar', width=38, command=self.guardar_producto)
        btn_nuevo_producto.grid(row=4, column=1, padx=10, pady=10)

        #llamamos a la funcion ultimo Producto
        self.ultimo_producto()

    def guardar_producto(self):
        #validamos para que no queden vacios los campos 
        if self.txt_codigo_nuevo_producto.get() == "" or self.txt_nombre_nuevo_producto.get() == "" or self.txt_precio_nuevo_producto.get() == "" or self.txt_stock_nuevo_producto.get() == "":
                messagebox.showwarning("Guardando Productos", "Por favor, complete todos los campos para guardar un nuevo Producto.")
                return
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Obtener los datos del nuevo producto
            datos_guardar_producto = (
            self.txt_codigo_nuevo_producto.get(),
            self.txt_nombre_nuevo_producto.get(),
            self.txt_precio_nuevo_producto.get(),
            self.txt_stock_nuevo_producto.get()
            )

            # Consultar la base de datos para insertar el nuevo producto
            miCursor.execute("INSERT INTO Productos VALUES(?,?,?,?)", datos_guardar_producto)
            messagebox.showinfo('Guardando Producto', "Producto Guardado Correctamente")
            # Aplicar cambios en la base de datos
            miConexion.commit()
            self.frame_nuevo_producto.destroy()#cerramos la ventana 
            self.ventana_lista_productos()#cargamos la ventana para ver los cambios 
            # Cerrar la conexión
            miConexion.close()

        except:
            messagebox.showerror("Guardando Producto", "Ocurrió un error al Guardar el Producto")

    def ultimo_producto(self):
        try:
            # Establecer la conexión 
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()
       
            # Consultar el máximo valor de Codigo en Productos
            miCursor.execute("SELECT MAX(Codigo) FROM Productos")
            # Obtener el máximo valor
            codprod = miCursor.fetchone()[0]

            # Si no hay registros o el máximo es None, establecer ultprod a 1
            if codprod is None:
                self.ultprod = 1
            else:
                self.ultprod = int(codprod) + 1

            # Configurar el estado de txt_codigo_nuevo_producto
            self.txt_codigo_nuevo_producto.configure(state=NORMAL)
            self.txt_codigo_nuevo_producto.insert(0, self.ultprod)
            self.txt_codigo_nuevo_producto.configure(state='readonly')

            # Aplicar cambios y cerrar la conexión
            miConexion.commit()
            miConexion.close()
        
        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Último Producto", "Ocurrió un error al obtener el último producto")

    def buscar_productos(self, event):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()
        
            # Limpiar el Treeview
            registros = self.tree_lista_productos.get_children()
            for elementos in registros:
                self.tree_lista_productos.delete(elementos)
        
            # Consultar la base de datos
            miCursor.execute("SELECT * FROM Productos WHERE Nombre LIKE ?", (self.txt_busqueda_productos.get() + '%',))
            # Obtener los registros y guardarlos en "datos"
            datos = miCursor.fetchall()
        
            # Llenar el Treeview con los resultados
            for row in datos:
                self.tree_lista_productos.insert("", 0, text=row[0], values=(row[0], row[1], row[2], row[3]))
        
            # Aplicar cambios y cerrar la conexión
            miConexion.commit()
            miConexion.close()
    
        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Búsqueda de Productos", "Ocurrió un error al buscar la lista de productos")

    def ventana_modificar_producto(self):
        # Validar que se haya seleccionado un producto
        self.producto_seleccionado = self.tree_lista_productos.focus()
        self.val_mod_prod = self.tree_lista_productos.item(self.producto_seleccionado, 'values')

        if self.val_mod_prod != '':
            self.frame_modificar_producto = Toplevel(self)
            self.frame_modificar_producto.title('Modificar Producto')
            self.frame_modificar_producto.geometry('460x300')
            self.frame_modificar_producto.resizable(0, 0)
            self.frame_modificar_producto.grab_set()

            lblframe_modificar_producto = LabelFrame(self.frame_modificar_producto)
            lblframe_modificar_producto.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

            lbl_codigo_modificar_producto = Label(lblframe_modificar_producto, text='Código')
            lbl_codigo_modificar_producto.grid(row=0, column=0, padx=10, pady=10)
            self.txt_codigo_modificar_producto = Entry(lblframe_modificar_producto, width=40)
            self.txt_codigo_modificar_producto.grid(row=0, column=1, padx=10, pady=10)

            lbl_nombre_modificar_producto = Label(lblframe_modificar_producto, text='Nombre')
            lbl_nombre_modificar_producto.grid(row=1, column=0, padx=10, pady=10)
            self.txt_nombre_modificar_producto = Entry(lblframe_modificar_producto, width=40)
            self.txt_nombre_modificar_producto.grid(row=1, column=1, padx=10, pady=10)

            lbl_precio_modificar_producto = Label(lblframe_modificar_producto, text='Precio')
            lbl_precio_modificar_producto.grid(row=2, column=0, padx=10, pady=10)
            self.txt_precio_modificar_producto = Entry(lblframe_modificar_producto, width=40)
            self.txt_precio_modificar_producto.grid(row=2, column=1, padx=10, pady=10)

            lbl_stock_modificar_producto = Label(lblframe_modificar_producto, text='Stock')
            lbl_stock_modificar_producto.grid(row=3, column=0, padx=10, pady=10)
            self.txt_stock_modificar_producto = Entry(lblframe_modificar_producto, width=40)
            self.txt_stock_modificar_producto.grid(row=3, column=1, padx=10, pady=10)

            btn_guardar_modificar_producto = ttk.Button(lblframe_modificar_producto, text='Modificar', width=38,
                                                        command=self.modificar_producto)
            btn_guardar_modificar_producto.grid(row=4, column=1, padx=10, pady=10)
            self.llenar_entrys_modificar_producto()

            # Llamar a la función cargar_datos_producto para cargar los datos del producto a modificar
            self.txt_nombre_modificar_producto.focus()

    def llenar_entrys_modificar_producto(self):
        # Limpiar todos los campos de entrada
        self.txt_codigo_modificar_producto.delete(0, END)
        self.txt_nombre_modificar_producto.delete(0, END)
        self.txt_precio_modificar_producto.delete(0, END)
        self.txt_stock_modificar_producto.delete(0, END)

        # Llenar los campos de entrada con los datos del producto seleccionado
        self.txt_codigo_modificar_producto.insert(0, self.val_mod_prod[0])
        self.txt_codigo_modificar_producto.config(state='readonly')
        self.txt_nombre_modificar_producto.insert(0, self.val_mod_prod[1])
        self.txt_precio_modificar_producto.insert(0, self.val_mod_prod[2])
        self.txt_stock_modificar_producto.insert(0, self.val_mod_prod[3])
    
    def modificar_producto(self):
        # Validar que no queden campos vacíos
        if self.txt_codigo_modificar_producto.get() == "" or self.txt_nombre_modificar_producto.get() == "" or self.txt_precio_modificar_producto.get() == "" or self.txt_stock_modificar_producto.get() == "":
            messagebox.showwarning("Modificar Producto", "Por favor, complete todos los campos para modificar un producto.")
            return

        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            datos_modificar_producto = (
                self.txt_nombre_modificar_producto.get(),
                self.txt_precio_modificar_producto.get(),
                self.txt_stock_modificar_producto.get()
            )

            # Consultar la base de datos para actualizar el producto
            miCursor.execute("UPDATE Productos SET Nombre=?,Precio=?,Stock=? WHERE Codigo=" + self.txt_codigo_modificar_producto.get(), datos_modificar_producto)
            messagebox.showinfo('Modificar Producto', "Producto Modificado Correctamente")
            # Aplicar cambios
            miConexion.commit()
            # Actualizar la vista de la lista de productos
            self.val_mod_prod = (
                self.txt_nombre_modificar_producto.get(),
                self.txt_precio_modificar_producto.get(),
                self.txt_stock_modificar_producto.get()
            )
            self.val_mod_prod=self.tree_lista_productos.item(self.producto_seleccionado,text='',values=
            (self.txt_codigo_modificar_producto.get(),self.txt_nombre_modificar_producto.get(),
            self.txt_precio_modificar_producto.get(),self.txt_stock_modificar_producto.get()))
            self.frame_modificar_producto.destroy()  # Cerrar la ventana de modificación
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Modificar Producto", "Ocurrió un error al modificar el producto")

    def ventana_eliminar_producto(self):
        # Validar que se haya seleccionado un producto
        self.producto_seleccionado = self.tree_lista_productos.focus()
        self.val_elim_prod = self.tree_lista_productos.item(self.producto_seleccionado, 'values')

        if self.val_elim_prod != '':
            self.frame_eliminar_producto = Toplevel(self)
            self.frame_eliminar_producto.title('Eliminar Producto')
            self.frame_eliminar_producto.geometry('460x250')
            self.frame_eliminar_producto.resizable(0, 0)
            self.frame_eliminar_producto.grab_set()

            lblframe_eliminar_producto = LabelFrame(self.frame_eliminar_producto)
            lblframe_eliminar_producto.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

            lbl_confirmacion = Label(lblframe_eliminar_producto, text='¿Está seguro que desea eliminar este producto?')
            lbl_confirmacion.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            lbl_nombre_producto = Label(lblframe_eliminar_producto, text='Nombre:')
            lbl_nombre_producto.grid(row=1, column=0, padx=10, pady=10)
            lbl_nombre_producto_valor = Label(lblframe_eliminar_producto, text=self.val_elim_prod[1])
            lbl_nombre_producto_valor.grid(row=1, column=1, padx=10, pady=10)

            lbl_precio_producto = Label(lblframe_eliminar_producto, text='Precio:')
            lbl_precio_producto.grid(row=2, column=0, padx=10, pady=10)
            lbl_precio_producto_valor = Label(lblframe_eliminar_producto, text=self.val_elim_prod[2])
            lbl_precio_producto_valor.grid(row=2, column=1, padx=10, pady=10)

            btn_eliminar_producto = ttk.Button(lblframe_eliminar_producto, text='Eliminar', width=38,
                                            style='danger', command=self.eliminar_producto)
            btn_eliminar_producto.grid(row=3, column=1, padx=10, pady=10)

    def eliminar_producto(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Obtener el código del producto a eliminar
            codigo_producto = self.val_elim_prod[0]

            # Consultar la base de datos para eliminar el producto
            miCursor.execute("DELETE FROM Productos WHERE Codigo=?", (codigo_producto,))
            messagebox.showinfo('Eliminar Producto', 'Producto Eliminado Correctamente')
            # Aplicar cambios
            miConexion.commit()
            # Actualizar la vista de la lista de productos
            self.tree_lista_productos.delete(self.producto_seleccionado)
            self.frame_eliminar_producto.destroy()  # Cerrar la ventana de eliminación
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror('Eliminar Producto', 'Ocurrió un error al eliminar el producto')


#====================================
#============ VENTAS ================
#====================================
    def ventana_lista_ventas(self):
        self.frame_lista_ventas = Frame(self.frame_center)
        self.frame_lista_ventas.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.lblframe_botones_listventas = LabelFrame(self.frame_lista_ventas)
        self.lblframe_botones_listventas.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        btn_nueva_venta = tb.Button(self.lblframe_botones_listventas, text='Nueva Venta', width=15, bootstyle="success",command=self.ventana_nueva_venta)
        btn_nueva_venta.grid(row=0, column=0, padx=5, pady=5)

        btn_modificar_venta = tb.Button(self.lblframe_botones_listventas, text='Modificar Venta', width=15, bootstyle="warning",command=self.ventana_modificar_venta)
        btn_modificar_venta.grid(row=0, column=1, padx=5, pady=5)

        btn_eliminar_venta = tb.Button(self.lblframe_botones_listventas, text='Eliminar Venta', width=15, bootstyle="danger",command=self.ventana_eliminar_venta)
        btn_eliminar_venta.grid(row=0, column=2, padx=5, pady=5)

        self.lblframe_busqueda_listventas = LabelFrame(self.frame_lista_ventas)
        self.lblframe_busqueda_listventas.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        self.txt_busqueda_ventas = ttk.Entry(self.lblframe_busqueda_listventas, width=73)
        self.txt_busqueda_ventas.grid(row=0, column=0, padx=5, pady=5)
        self.txt_busqueda_ventas.bind('<Key>',self.buscar_ventas)

        self.lblframe_tree_listventas = LabelFrame(self.frame_lista_ventas)
        self.lblframe_tree_listventas.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        columnas = ("codigo_venta", "fecha", "total")

        self.tree_lista_ventas = tb.Treeview(self.lblframe_tree_listventas, columns=columnas,
                                         height=17, show='headings', bootstyle='dark')
        self.tree_lista_ventas.grid(row=0, column=0)

        self.tree_lista_ventas.heading("codigo_venta", text="Codigo Venta", anchor=W)
        self.tree_lista_ventas.heading("fecha", text="Fecha", anchor=W)
        self.tree_lista_ventas.heading("total", text="Total", anchor=W)
        self.tree_lista_ventas['displaycolumns'] = ("codigo_venta", "fecha", "total")

        # crear el scrollbar
        tree_scroll_listventas = tb.Scrollbar(self.frame_lista_ventas, bootstyle="round-success")
        tree_scroll_listventas.grid(row=2, column=1)

        # configurar el scrollbar
        tree_scroll_listventas.config(command=self.tree_lista_ventas.yview)

        #Llamamos a nuestra funcion mostrar productos
        self.mostrar_ventas()

    def ventana_nueva_venta(self):
        self.frame_nueva_venta = Toplevel(self)
        self.frame_nueva_venta.title('Nueva Venta')
        self.frame_nueva_venta.geometry('490x300')
        self.frame_nueva_venta.resizable(0, 0)
        self.frame_nueva_venta.grab_set()

        lblframe_nueva_venta = LabelFrame(self.frame_nueva_venta)
        lblframe_nueva_venta.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        lbl_codigo_venta = Label(lblframe_nueva_venta, text='Codigo Venta')
        lbl_codigo_venta.grid(row=0, column=0, padx=10, pady=10)
        self.txt_codigo_venta = Entry(lblframe_nueva_venta, width=40)
        self.txt_codigo_venta.grid(row=0, column=1, padx=10, pady=10)

        lbl_fecha_venta = Label(lblframe_nueva_venta, text='Fecha Venta')
        lbl_fecha_venta.grid(row=1, column=0, padx=10, pady=10)
        self.txt_fecha_venta = Entry(lblframe_nueva_venta, width=40)
        self.txt_fecha_venta.grid(row=1, column=1, padx=10, pady=10)

        lbl_total_venta = Label(lblframe_nueva_venta, text='Total Venta')
        lbl_total_venta.grid(row=2, column=0, padx=10, pady=10)
        self.txt_total_venta = Entry(lblframe_nueva_venta, width=40)
        self.txt_total_venta.grid(row=2, column=1, padx=10, pady=10)

        btn_guardar_venta = ttk.Button(lblframe_nueva_venta, text='Guardar', width=38, command=self.guardar_venta)
        btn_guardar_venta.grid(row=4, column=1, padx=10, pady=10)
        #llamamos a la funcion ultimo venta
        self.ultimo_venta()

    def guardar_venta(self):
        #validamos para que no queden vacios los campos 
        if self.txt_codigo_venta.get() == "" or self.txt_fecha_venta.get() == "" or self.txt_total_venta.get() == "":
                messagebox.showwarning("Guardando Usuarios", "Por favor, complete todos los campos para guardar un nuevo usuario.")
                return
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Obtener los datos de la nueva venta
            datos_guardar_venta = (
            self.txt_codigo_venta.get(),
            self.txt_fecha_venta.get(),
            self.txt_total_venta.get()
            )

            # Consultar la base de datos para insertar la nueva venta
            miCursor.execute("INSERT INTO Ventas VALUES(?,?,?)", datos_guardar_venta)
            messagebox.showinfo('Guardando Venta', "Venta Guardada Correctamente")
            # Aplicar cambios en la base de datos
            miConexion.commit()
            self.frame_nueva_venta.destroy()#cerramos la ventana 
            self.ventana_lista_ventas()#cargamos la ventana para ver los cambios 
            # Cerrar la conexión
            miConexion.close()

        except:
            messagebox.showerror("Guardando Venta", "Ocurrió un error al Guardar la Venta")

    def mostrar_ventas(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()
            # Limpiar el treeview de ventas
            registros = self.tree_lista_ventas.get_children()
            for elemento in registros:
                self.tree_lista_ventas.delete(elemento)
            # Consultar la base de datos para obtener las ventas
            miCursor.execute("SELECT * FROM Ventas")
            # Obtener los registros y guardarlos en "datos"
            datos = miCursor.fetchall()
            # Recorrer cada fila encontrada
            for row in datos:
                # Llenar el treeview con los datos de las ventas
                self.tree_lista_ventas.insert("", 0, text=row[0], values=(row[0], row[1], row[2]))
            # Aplicar cambios en la interfaz
            miConexion.commit()
            # Cerrar la conexión
            miConexion.close()
        except:
            messagebox.showerror("Lista de Ventas", "Ocurrió un error al mostrar la lista de ventas")

    def ultimo_venta(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Consultar el máximo valor de Codigo en Ventas
            miCursor.execute("SELECT MAX(`Codigo Venta`) FROM Ventas")
            # Obtener el máximo valor
            codventa = miCursor.fetchone()[0]

            # Si no hay registros o el máximo es None, establecer ultventa a 1
            if codventa is None:
                self.ultventa = 1
            else:
                self.ultventa = int(codventa) + 1

            # Configurar el estado de txt_codigo_nueva_venta
            self.txt_codigo_venta.configure(state=NORMAL)
            self.txt_codigo_venta.insert(0, self.ultventa)
            self.txt_codigo_venta.configure(state='readonly')

            # Aplicar cambios y cerrar la conexión
            miConexion.commit()
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Último Código de Venta", "Ocurrió un error al obtener el último código de venta")

    def buscar_ventas(self, event):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Limpiar el Treeview
            registros = self.tree_lista_ventas.get_children()
            for elementos in registros:
                self.tree_lista_ventas.delete(elementos)

            # Consultar la base de datos con el código de venta exacto
            codigo_venta = self.txt_busqueda_ventas.get()
            miCursor.execute("SELECT * FROM Ventas WHERE `Codigo Venta` = ?", (codigo_venta,))
            # Obtener los registros y guardarlos en "datos"
            datos = miCursor.fetchall()

            # Llenar el Treeview con los resultados
            for row in datos:
                self.tree_lista_ventas.insert("", 0, text=row[0], values=(row[0], row[1], row[2]))

            # Aplicar cambios y cerrar la conexión
            miConexion.commit()
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Búsqueda de Ventas", "Ocurrió un error al buscar la lista de ventas")

    def ventana_modificar_venta(self):
        # Validar que se haya seleccionado una venta
        self.venta_seleccionada = self.tree_lista_ventas.focus()
        self.val_mod_venta = self.tree_lista_ventas.item(self.venta_seleccionada, 'values')

        if self.val_mod_venta != '':
            self.frame_modificar_venta = Toplevel(self)
            self.frame_modificar_venta.title('Modificar Venta')
            self.frame_modificar_venta.geometry('500x300')
            self.frame_modificar_venta.resizable(0, 0)
            self.frame_modificar_venta.grab_set()

            lblframe_modificar_venta = LabelFrame(self.frame_modificar_venta)
            lblframe_modificar_venta.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

            lbl_codigo_modificar_venta = Label(lblframe_modificar_venta, text='Codigo Venta')
            lbl_codigo_modificar_venta.grid(row=0, column=0, padx=10, pady=10)
            self.txt_codigo_modificar_venta = Entry(lblframe_modificar_venta, width=40)
            self.txt_codigo_modificar_venta.grid(row=0, column=1, padx=10, pady=10)

            lbl_fecha_modificar_venta = Label(lblframe_modificar_venta, text='Fecha Venta')
            lbl_fecha_modificar_venta.grid(row=1, column=0, padx=10, pady=10)
            self.txt_fecha_modificar_venta = Entry(lblframe_modificar_venta, width=40)
            self.txt_fecha_modificar_venta.grid(row=1, column=1, padx=10, pady=10)

            lbl_total_modificar_venta = Label(lblframe_modificar_venta, text='Total Venta')
            lbl_total_modificar_venta.grid(row=2, column=0, padx=10, pady=10)
            self.txt_total_modificar_venta = Entry(lblframe_modificar_venta, width=40)
            self.txt_total_modificar_venta.grid(row=2, column=1, padx=10, pady=10)

            btn_guardar_modificar_venta = ttk.Button(lblframe_modificar_venta, text='Modificar', width=38,
                                                    command=self.modificar_venta)
            btn_guardar_modificar_venta.grid(row=4, column=1, padx=10, pady=10)
            self.llenar_entrys_modificar_venta()

            # Llamar a la función cargar_datos_venta para cargar los datos de la venta a modificar
            self.txt_fecha_modificar_venta.focus()

    def llenar_entrys_modificar_venta(self):
        # Limpiar todos los campos de entrada
        self.txt_codigo_modificar_venta.delete(0, END)
        self.txt_fecha_modificar_venta.delete(0, END)
        self.txt_total_modificar_venta.delete(0, END)

        # Llenar los campos de entrada con los datos de la venta seleccionada
        self.txt_codigo_modificar_venta.insert(0, self.val_mod_venta[0])
        self.txt_codigo_modificar_venta.config(state='readonly')
        self.txt_fecha_modificar_venta.insert(0, self.val_mod_venta[1])
        self.txt_total_modificar_venta.insert(0, self.val_mod_venta[2])

    def modificar_venta(self):
        # Validar que no queden campos vacíos
        if self.txt_codigo_modificar_venta.get() == "" or self.txt_fecha_modificar_venta.get() == "" or self.txt_total_modificar_venta.get() == "":
            messagebox.showwarning("Modificar Venta", "Por favor, complete todos los campos para modificar una venta.")
            return

        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            datos_modificar_venta = (
                self.txt_fecha_modificar_venta.get(),
                self.txt_total_modificar_venta.get()
            )

            # Consultar la base de datos para actualizar la venta
            miCursor.execute("UPDATE Ventas SET Fecha=?,Total=? WHERE 'Codigo Venta'=" + self.txt_codigo_modificar_venta.get(), datos_modificar_venta)
            messagebox.showinfo('Modificar Venta', "Venta Modificada Correctamente")
            # Aplicar cambios
            miConexion.commit()
            # Actualizar la vista de la lista de ventas
            self.val_mod_venta = (
                self.txt_fecha_modificar_venta.get(),
                self.txt_total_modificar_venta.get()
            )
            self.val_mod_venta=self.tree_lista_ventas.item(self.venta_seleccionada,text='',values=
            (self.txt_codigo_modificar_venta.get(),self.txt_fecha_modificar_venta.get(),
            self.txt_total_modificar_venta.get()))
            self.frame_modificar_venta.destroy()  # Cerrar la ventana de modificación
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Modificar Venta", "Ocurrió un error al modificar la venta")

    def ventana_eliminar_venta(self):
        # Validar que se haya seleccionado una venta
        self.venta_seleccionada = self.tree_lista_ventas.focus()
        self.val_elim_venta = self.tree_lista_ventas.item(self.venta_seleccionada, 'values')

        if self.val_elim_venta != '':
            self.frame_eliminar_venta = Toplevel(self)
            self.frame_eliminar_venta.title('Eliminar Venta')
            self.frame_eliminar_venta.geometry('460x250')
            self.frame_eliminar_venta.resizable(0, 0)
            self.frame_eliminar_venta.grab_set()

            lblframe_eliminar_venta = LabelFrame(self.frame_eliminar_venta)
            lblframe_eliminar_venta.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

            lbl_confirmacion = Label(lblframe_eliminar_venta, text='¿Está seguro que desea eliminar esta venta?')
            lbl_confirmacion.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            lbl_fecha_venta = Label(lblframe_eliminar_venta, text='Fecha:')
            lbl_fecha_venta.grid(row=1, column=0, padx=10, pady=10)
            lbl_fecha_venta_valor = Label(lblframe_eliminar_venta, text=self.val_elim_venta[1])
            lbl_fecha_venta_valor.grid(row=1, column=1, padx=10, pady=10)

            lbl_total_venta = Label(lblframe_eliminar_venta, text='Total:')
            lbl_total_venta.grid(row=2, column=0, padx=10, pady=10)
            lbl_total_venta_valor = Label(lblframe_eliminar_venta, text=self.val_elim_venta[2])
            lbl_total_venta_valor.grid(row=2, column=1, padx=10, pady=10)

            btn_eliminar_venta = ttk.Button(lblframe_eliminar_venta, text='Eliminar', width=38,
                                            style='danger', command=self.eliminar_venta)
            btn_eliminar_venta.grid(row=3, column=1, padx=10, pady=10)

    def eliminar_venta(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Obtener el código de la venta a eliminar
            codigo_venta = self.val_elim_venta[0]

            # Consultar la base de datos para eliminar la venta
            miCursor.execute("DELETE FROM Ventas WHERE 'Codigo Venta'=?", (codigo_venta,))
            messagebox.showinfo('Eliminar Venta', 'Venta Eliminada Correctamente')
            # Aplicar cambios
            miConexion.commit()
            # Actualizar la vista de la lista de ventas
            self.tree_lista_ventas.delete(self.venta_seleccionada)
            self.frame_eliminar_venta.destroy()  # Cerrar la ventana de eliminación
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror('Eliminar Venta', 'Ocurrió un error al eliminar la venta')

    
#====================================
#============ CLIENTES ==============
#====================================
    def ventana_lista_clientes(self):
        self.frame_lista_clientes = Frame(self.frame_center)
        self.frame_lista_clientes.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.lblframe_botones_listclientes = LabelFrame(self.frame_lista_clientes)
        self.lblframe_botones_listclientes.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        btn_nuevo_cliente = tb.Button(self.lblframe_botones_listclientes, text='Nuevo Cliente', width=15, bootstyle="success",command=self.ventana_nuevo_cliente)
        btn_nuevo_cliente.grid(row=0, column=0, padx=5, pady=5)

        btn_modificar_cliente = tb.Button(self.lblframe_botones_listclientes, text='Modificar Cliente', width=15, bootstyle="warning",command=self.ventana_modificar_cliente)
        btn_modificar_cliente.grid(row=0, column=1, padx=5, pady=5)

        btn_eliminar_cliente = tb.Button(self.lblframe_botones_listclientes, text='Eliminar Cliente', width=15, bootstyle="danger",command=self.ventana_eliminar_cliente)
        btn_eliminar_cliente.grid(row=0, column=2, padx=5, pady=5)

        self.lblframe_busqueda_listclientes = LabelFrame(self.frame_lista_clientes)
        self.lblframe_busqueda_listclientes.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        self.txt_busqueda_clientes = ttk.Entry(self.lblframe_busqueda_listclientes, width=73)
        self.txt_busqueda_clientes.grid(row=0, column=0, padx=5, pady=5)
        self.txt_busqueda_clientes.bind('<Key>',self.buscar_clientes)


        self.lblframe_tree_listclientes = LabelFrame(self.frame_lista_clientes)
        self.lblframe_tree_listclientes.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        columnas = ("codigo_cliente", "nombre", "telefono", "direccion")

        self.tree_lista_clientes = tb.Treeview(self.lblframe_tree_listclientes, columns=columnas,
                                            height=17, show='headings', bootstyle='dark')
        self.tree_lista_clientes.grid(row=0, column=0)

        self.tree_lista_clientes.heading("codigo_cliente", text="Codigo Cliente", anchor=W)
        self.tree_lista_clientes.heading("nombre", text="Nombre", anchor=W)
        self.tree_lista_clientes.heading("telefono", text="Telefono", anchor=W)
        self.tree_lista_clientes.heading("direccion", text="Direccion", anchor=W)
        self.tree_lista_clientes['displaycolumns'] = ("codigo_cliente", "nombre", "telefono", "direccion")

        # crear el scrollbar
        tree_scroll_listclientes = tb.Scrollbar(self.frame_lista_clientes, bootstyle="round-success")
        tree_scroll_listclientes.grid(row=2, column=1)

        # configurar el scrollbar
        tree_scroll_listclientes.config(command=self.tree_lista_clientes.yview)
        
        #Llamamos a nuestra funcion mostrar productos
        self.mostrar_clientes()

    def mostrar_clientes(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()
            # Limpiar el treeview de clientes
            registros = self.tree_lista_clientes.get_children()
            for elemento in registros:
                self.tree_lista_clientes.delete(elemento)
            # Consultar la base de datos para obtener los clientes
            miCursor.execute("SELECT * FROM Clientes")
            # Obtener los registros y guardarlos en "datos"
            datos = miCursor.fetchall()
            # Recorrer cada fila encontrada
            for row in datos:
                # Llenar el treeview con los datos de los clientes
                self.tree_lista_clientes.insert("", 0, text=row[0], values=(row[0], row[1], row[2], row[3]))
            # Aplicar cambios en la interfaz
            miConexion.commit()
            # Cerrar la conexión
            miConexion.close()
        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Lista de Clientes", "Ocurrió un error al mostrar la lista de clientes")

    def ventana_nuevo_cliente(self):
        self.frame_nuevo_cliente = Toplevel(self)
        self.frame_nuevo_cliente.title('Nuevo Cliente')
        self.frame_nuevo_cliente.geometry('510x300')
        self.frame_nuevo_cliente.resizable(0, 0)
        self.frame_nuevo_cliente.grab_set()

        lblframe_nuevo_cliente = LabelFrame(self.frame_nuevo_cliente)
        lblframe_nuevo_cliente.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        lbl_codigo_cliente = Label(lblframe_nuevo_cliente, text='Codigo Cliente')
        lbl_codigo_cliente.grid(row=0, column=0, padx=10, pady=10)
        self.txt_codigo_cliente = Entry(lblframe_nuevo_cliente, width=40)
        self.txt_codigo_cliente.grid(row=0, column=1, padx=10, pady=10)

        lbl_nombre_cliente = Label(lblframe_nuevo_cliente, text='Nombre Cliente')
        lbl_nombre_cliente.grid(row=1, column=0, padx=10, pady=10)
        self.txt_nombre_cliente = Entry(lblframe_nuevo_cliente, width=40)
        self.txt_nombre_cliente.grid(row=1, column=1, padx=10, pady=10)

        lbl_telefono_cliente = Label(lblframe_nuevo_cliente, text='Teléfono Cliente')
        lbl_telefono_cliente.grid(row=2, column=0, padx=10, pady=10)
        self.txt_telefono_cliente = Entry(lblframe_nuevo_cliente, width=40)
        self.txt_telefono_cliente.grid(row=2, column=1, padx=10, pady=10)

        
        lbl_direccion_cliente = Label(lblframe_nuevo_cliente, text='Direccion')
        lbl_direccion_cliente.grid(row=3, column=0, padx=10, pady=10)
        self.txt_direccion_cliente = Entry(lblframe_nuevo_cliente, width=40)
        self.txt_direccion_cliente.grid(row=3, column=1, padx=10, pady=10)


        btn_guardar_cliente = ttk.Button(lblframe_nuevo_cliente, text='Guardar', width=38, command=self.guardar_cliente)
        btn_guardar_cliente.grid(row=4, column=1, padx=10, pady=10)
        # Llamamos a la función ultimo_cliente
        self.ultimo_cliente()

    def guardar_cliente(self):
            # Validamos para que no queden vacíos los campos
        if self.txt_codigo_cliente.get() == "" or self.txt_nombre_cliente.get() == "" or self.txt_telefono_cliente.get() == "" or self.txt_direccion_cliente.get() == "":
                messagebox.showwarning("Guardando Cliente", "Por favor, complete todos los campos para guardar un nuevo cliente.")
                return
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Obtener los datos del nuevo cliente
            datos_guardar_cliente = (
            self.txt_codigo_cliente.get(),
            self.txt_nombre_cliente.get(),
            self.txt_telefono_cliente.get(),
            self.txt_direccion_cliente.get()
            )

            # Consultar la base de datos para insertar el nuevo cliente
            miCursor.execute("INSERT INTO Clientes VALUES(?,?,?,?)", datos_guardar_cliente)
            messagebox.showinfo('Guardando Cliente', "Cliente Guardado Correctamente")
            # Aplicar cambios en la base de datos
            miConexion.commit()
            self.frame_nuevo_cliente.destroy()  # Cerramos la ventana
            self.ventana_lista_clientes()  # Cargamos la ventana para ver los cambios
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Guardando Cliente", "Ocurrió un error al guardar el cliente")

    def ultimo_cliente(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Consultar el máximo valor de CodigoCliente en Clientes
            miCursor.execute("SELECT MAX(`Codigo Cliente`) FROM Clientes")
            # Obtener el máximo valor
            codcliente = miCursor.fetchone()[0]

            # Si no hay registros o el máximo es None, establecer ultcliente a 1
            if codcliente is None:
                self.ultcliente = 1
            else:
                self.ultcliente = int(codcliente) + 1

            # Configurar el estado de txt_codigo_cliente
            self.txt_codigo_cliente.configure(state=NORMAL)
            self.txt_codigo_cliente.insert(0, self.ultcliente)
            self.txt_codigo_cliente.configure(state='readonly')

            # Aplicar cambios y cerrar la conexión
            miConexion.commit()
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Último Código de Cliente", "Ocurrió un error al obtener el último código de cliente")

    def buscar_clientes(self, event):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Limpiar el Treeview
            registros = self.tree_lista_clientes.get_children()
            for elementos in registros:
                self.tree_lista_clientes.delete(elementos)

            # Consultar la base de datos
            miCursor.execute("SELECT * FROM Clientes WHERE Nombre LIKE ?", (self.txt_busqueda_clientes.get() + '%',))
            # Obtener los registros y guardarlos en "datos"
            datos = miCursor.fetchall()

            # Llenar el Treeview con los resultados
            for row in datos:
                self.tree_lista_clientes.insert("", 0, text=row[0], values=(row[0], row[1], row[2], row[3]))

            # Aplicar cambios y cerrar la conexión
            miConexion.commit()
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Búsqueda de Clientes", "Ocurrió un error al buscar la lista de clientes")

    def ventana_modificar_cliente(self):
        # Validar que se haya seleccionado un cliente
        self.cliente_seleccionado = self.tree_lista_clientes.focus()
        self.val_mod_cliente = self.tree_lista_clientes.item(self.cliente_seleccionado, 'values')

        if self.val_mod_cliente != '':
            self.frame_modificar_cliente = Toplevel(self)
            self.frame_modificar_cliente.title('Modificar Cliente')
            self.frame_modificar_cliente.geometry('510x300')
            self.frame_modificar_cliente.resizable(0, 0)
            self.frame_modificar_cliente.grab_set()

            lblframe_modificar_cliente = LabelFrame(self.frame_modificar_cliente)
            lblframe_modificar_cliente.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

            lbl_codigo_modificar_cliente = Label(lblframe_modificar_cliente, text='Codigo Cliente')
            lbl_codigo_modificar_cliente.grid(row=0, column=0, padx=10, pady=10)
            self.txt_codigo_modificar_cliente = Entry(lblframe_modificar_cliente, width=40)
            self.txt_codigo_modificar_cliente.grid(row=0, column=1, padx=10, pady=10)

            lbl_nombre_modificar_cliente = Label(lblframe_modificar_cliente, text='Nombre Cliente')
            lbl_nombre_modificar_cliente.grid(row=1, column=0, padx=10, pady=10)
            self.txt_nombre_modificar_cliente = Entry(lblframe_modificar_cliente, width=40)
            self.txt_nombre_modificar_cliente.grid(row=1, column=1, padx=10, pady=10)

            lbl_telefono_modificar_cliente = Label(lblframe_modificar_cliente, text='Teléfono Cliente')
            lbl_telefono_modificar_cliente.grid(row=2, column=0, padx=10, pady=10)
            self.txt_telefono_modificar_cliente = Entry(lblframe_modificar_cliente, width=40)
            self.txt_telefono_modificar_cliente.grid(row=2, column=1, padx=10, pady=10)

            lbl_direccion_modificar_cliente = Label(lblframe_modificar_cliente, text='Dirección Cliente')
            lbl_direccion_modificar_cliente.grid(row=3, column=0, padx=10, pady=10)
            self.txt_direccion_modificar_cliente = Entry(lblframe_modificar_cliente, width=40)
            self.txt_direccion_modificar_cliente.grid(row=3, column=1, padx=10, pady=10)

            btn_guardar_modificar_cliente = ttk.Button(lblframe_modificar_cliente, text='Modificar', width=38,
                                                        command=self.modificar_cliente)
            btn_guardar_modificar_cliente.grid(row=4, column=1, padx=10, pady=10)
            self.llenar_entrys_modificar_cliente()

            # Llamar a la función cargar_datos_cliente para cargar los datos del cliente a modificar
            self.txt_nombre_modificar_cliente.focus()

    def llenar_entrys_modificar_cliente(self):
        # Limpiar todos los campos de entrada
        self.txt_codigo_modificar_cliente.delete(0, END)
        self.txt_nombre_modificar_cliente.delete(0, END)
        self.txt_telefono_modificar_cliente.delete(0, END)
        self.txt_direccion_modificar_cliente.delete(0, END)

        # Llenar los campos de entrada con los datos del cliente seleccionado
        self.txt_codigo_modificar_cliente.insert(0, self.val_mod_cliente[0])
        self.txt_codigo_modificar_cliente.config(state='readonly')
        self.txt_nombre_modificar_cliente.insert(0, self.val_mod_cliente[1])
        self.txt_telefono_modificar_cliente.insert(0, self.val_mod_cliente[2])
        self.txt_direccion_modificar_cliente.insert(0, self.val_mod_cliente[3])

    def modificar_cliente(self):
        # Validar que no queden campos vacíos
        if self.txt_codigo_modificar_cliente.get() == "" or self.txt_nombre_modificar_cliente.get() == "" or self.txt_telefono_modificar_cliente.get() == "" or self.txt_direccion_modificar_cliente.get() == "":
            messagebox.showwarning("Modificar Cliente", "Por favor, complete todos los campos para modificar un cliente.")
            return

        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            datos_modificar_cliente = (
                self.txt_nombre_modificar_cliente.get(),
                self.txt_telefono_modificar_cliente.get(),
                self.txt_direccion_modificar_cliente.get()
            )

            # Consultar la base de datos para actualizar el cliente
            miCursor.execute("UPDATE Clientes SET Nombre=?,Telefono=?,Direccion=? WHERE 'Codigo Cliente'=" + self.txt_codigo_modificar_cliente.get(), datos_modificar_cliente)
            messagebox.showinfo('Modificar Cliente', "Cliente Modificado Correctamente")
            # Aplicar cambios
            miConexion.commit()
            # Actualizar la vista de la lista de clientes
            self.val_mod_cliente = (
                self.txt_nombre_modificar_cliente.get(),
                self.txt_telefono_modificar_cliente.get(),
                self.txt_direccion_modificar_cliente.get()
            )
            self.val_mod_cliente = self.tree_lista_clientes.item(self.cliente_seleccionado, text='', values=
            (self.txt_codigo_modificar_cliente.get(), self.txt_nombre_modificar_cliente.get(),
            self.txt_telefono_modificar_cliente.get(), self.txt_direccion_modificar_cliente.get()))
            self.frame_modificar_cliente.destroy()  # Cerrar la ventana de modificación
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Modificar Cliente", "Ocurrió un error al modificar el cliente")

    def ventana_eliminar_cliente(self):
        # Validar que se haya seleccionado un cliente
        self.cliente_seleccionado = self.tree_lista_clientes.focus()
        self.val_elim_cliente = self.tree_lista_clientes.item(self.cliente_seleccionado, 'values')

        if self.val_elim_cliente != '':
            self.frame_eliminar_cliente = Toplevel(self)
            self.frame_eliminar_cliente.title('Eliminar Cliente')
            self.frame_eliminar_cliente.geometry('460x250')
            self.frame_eliminar_cliente.resizable(0, 0)
            self.frame_eliminar_cliente.grab_set()

            lblframe_eliminar_cliente = LabelFrame(self.frame_eliminar_cliente)
            lblframe_eliminar_cliente.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

            lbl_confirmacion = Label(lblframe_eliminar_cliente, text='¿Está seguro que desea eliminar este cliente?')
            lbl_confirmacion.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            lbl_nombre_cliente = Label(lblframe_eliminar_cliente, text='Nombre:')
            lbl_nombre_cliente.grid(row=1, column=0, padx=10, pady=10)
            lbl_nombre_cliente_valor = Label(lblframe_eliminar_cliente, text=self.val_elim_cliente[1])
            lbl_nombre_cliente_valor.grid(row=1, column=1, padx=10, pady=10)

            lbl_telefono_cliente = Label(lblframe_eliminar_cliente, text='Teléfono:')
            lbl_telefono_cliente.grid(row=2, column=0, padx=10, pady=10)
            lbl_telefono_cliente_valor = Label(lblframe_eliminar_cliente, text=self.val_elim_cliente[2])
            lbl_telefono_cliente_valor.grid(row=2, column=1, padx=10, pady=10)

            btn_eliminar_cliente = ttk.Button(lblframe_eliminar_cliente, text='Eliminar', width=38,
                                            style='danger', command=self.eliminar_cliente)
            btn_eliminar_cliente.grid(row=3, column=1, padx=10, pady=10)

    def eliminar_cliente(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Obtener el código del cliente a eliminar
            codigo_cliente = self.val_elim_cliente[0]

            # Consultar la base de datos para eliminar el cliente
            miCursor.execute("DELETE FROM Clientes WHERE 'Codigo Cliente'=?", (codigo_cliente,))
            messagebox.showinfo('Eliminar Cliente', 'Cliente Eliminado Correctamente')
            # Aplicar cambios
            miConexion.commit()
            # Actualizar la vista de la lista de clientes
            self.tree_lista_clientes.delete(self.cliente_seleccionado)
            self.frame_eliminar_cliente.destroy()  # Cerrar la ventana de eliminación
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror('Eliminar Cliente', 'Ocurrió un error al eliminar el cliente')


#====================================
#============ COMPRAS ===============
#====================================
    def ventana_lista_compras(self):
        self.frame_lista_compras = Frame(self.frame_center)
        self.frame_lista_compras.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.lblframe_botones_listcompras = LabelFrame(self.frame_lista_compras)
        self.lblframe_botones_listcompras.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        btn_nueva_compra = tb.Button(self.lblframe_botones_listcompras, text='Nueva Compra', width=15, bootstyle="success", command=self.ventana_nueva_compra)
        btn_nueva_compra.grid(row=0, column=0, padx=5, pady=5)

        btn_modificar_compra = tb.Button(self.lblframe_botones_listcompras, text='Modificar Compra', width=15, bootstyle="warning",command=self.ventana_modificar_compra)
        btn_modificar_compra.grid(row=0, column=1, padx=5, pady=5)

        btn_eliminar_compra = tb.Button(self.lblframe_botones_listcompras, text='Eliminar Compra', width=15, bootstyle="danger",command=self.ventana_eliminar_compra)
        btn_eliminar_compra.grid(row=0, column=2, padx=5, pady=5)

        self.lblframe_busqueda_listcompras = LabelFrame(self.frame_lista_compras)
        self.lblframe_busqueda_listcompras.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        txt_busqueda_compras = ttk.Entry(self.lblframe_busqueda_listcompras, width=73)
        txt_busqueda_compras.grid(row=0, column=0, padx=5, pady=5)

        self.lblframe_tree_listcompras = LabelFrame(self.frame_lista_compras)
        self.lblframe_tree_listcompras.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        columnas = ("codigo_compra", "fecha", "total")

        self.tree_lista_compras = tb.Treeview(self.lblframe_tree_listcompras, columns=columnas,
                                           height=17, show='headings', bootstyle='dark')
        self.tree_lista_compras.grid(row=0, column=0)

        self.tree_lista_compras.heading("codigo_compra", text="Codigo Compra", anchor=W)
        self.tree_lista_compras.heading("fecha", text="Fecha", anchor=W)
        self.tree_lista_compras.heading("total", text="Total", anchor=W)
        self.tree_lista_compras['displaycolumns'] = ("codigo_compra", "fecha", "total")

        # crear el scrollbar
        tree_scroll_listcompras = tb.Scrollbar(self.frame_lista_compras, bootstyle="round-success")
        tree_scroll_listcompras.grid(row=2, column=1)

        # configurar el scrollbar
        tree_scroll_listcompras.config(command=self.tree_lista_compras.yview)

         
        #Llamamos a nuestra funcion mostrar productos
        self.mostrar_compras()

    def mostrar_compras(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()
            # Limpiar el treeview de compras
            registros = self.tree_lista_compras.get_children()
            for elemento in registros:
                self.tree_lista_compras.delete(elemento)
            # Consultar la base de datos para obtener las compras
            miCursor.execute("SELECT * FROM Compras")
            # Obtener los registros y guardarlos en "datos"
            datos = miCursor.fetchall()
            # Recorrer cada fila encontrada
            for row in datos:
                # Llenar el treeview con los datos de las compras
                self.tree_lista_compras.insert("", 0, text=row[0], values=(row[0], row[1], row[2]))
            # Aplicar cambios en la interfaz
            miConexion.commit()
            # Cerrar la conexión
            miConexion.close()
        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Lista de Compras", "Ocurrió un error al mostrar la lista de compras")

    def ventana_nueva_compra(self):
        self.frame_nueva_compra = Toplevel(self)
        self.frame_nueva_compra.title('Nueva Compra')
        self.frame_nueva_compra.geometry('510x300')
        self.frame_nueva_compra.resizable(0, 0)
        self.frame_nueva_compra.grab_set()

        lblframe_nueva_compra = LabelFrame(self.frame_nueva_compra)
        lblframe_nueva_compra.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        lbl_codigo_compra = Label(lblframe_nueva_compra, text='Codigo Compra')
        lbl_codigo_compra.grid(row=0, column=0, padx=10, pady=10)
        self.txt_codigo_compra = Entry(lblframe_nueva_compra, width=40)
        self.txt_codigo_compra.grid(row=0, column=1, padx=10, pady=10)

        lbl_fecha_compra = Label(lblframe_nueva_compra, text='Fecha Compra')
        lbl_fecha_compra.grid(row=1, column=0, padx=10, pady=10)
        self.txt_fecha_compra = Entry(lblframe_nueva_compra, width=40)
        self.txt_fecha_compra.grid(row=1, column=1, padx=10, pady=10)

        lbl_total_compra = Label(lblframe_nueva_compra, text='Total Compra')
        lbl_total_compra.grid(row=2, column=0, padx=10, pady=10)
        self.txt_total_compra = Entry(lblframe_nueva_compra, width=40)
        self.txt_total_compra.grid(row=2, column=1, padx=10, pady=10)

        btn_guardar_compra = ttk.Button(lblframe_nueva_compra, text='Guardar', width=38, command=self.guardar_compra)
        btn_guardar_compra.grid(row=4, column=1, padx=10, pady=10)
        # Llamamos a la función ultimo_compra
        self.ultimo_compra()

    def guardar_compra(self):
        # Validamos para que no queden vacíos los campos
        if self.txt_codigo_compra.get() == "" or self.txt_fecha_compra.get() == "" or self.txt_total_compra.get() == "":
            messagebox.showwarning("Guardando Compra", "Por favor, complete todos los campos para guardar una nueva compra.")
            return
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Obtener los datos de la nueva compra
            datos_guardar_compra = (
            self.txt_codigo_compra.get(),
            self.txt_fecha_compra.get(),
            self.txt_total_compra.get()
            )

            # Consultar la base de datos para insertar la nueva compra
            miCursor.execute("INSERT INTO Compras VALUES(?,?,?)", datos_guardar_compra)
            messagebox.showinfo('Guardando Compra', "Compra Guardada Correctamente")
            # Aplicar cambios en la base de datos
            miConexion.commit()
            self.frame_nueva_compra.destroy()  # Cerramos la ventana
            self.ventana_lista_compras()  # Cargamos la ventana para ver los cambios
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Guardando Compra", "Ocurrió un error al guardar la compra")

    def ultimo_compra(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Consultar el máximo valor de CodigoCompra en Compra
            miCursor.execute("SELECT MAX(`Codigo Compra`) FROM Compras")
            # Obtener el máximo valor
            codcompra = miCursor.fetchone()[0]

            # Si no hay registros o el máximo es None, establecer ultcompra a 1
            if codcompra is None:
                self.ultcompra = 1
            else:
                self.ultcompra = int(codcompra) + 1

            # Configurar el estado de txt_codigo_compra
            self.txt_codigo_compra.configure(state=NORMAL)
            self.txt_codigo_compra.insert(0, self.ultcompra)
            self.txt_codigo_compra.configure(state='readonly')

            # Aplicar cambios y cerrar la conexión
            miConexion.commit()
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Último Código de Compra", "Ocurrió un error al obtener el último código de compra")

    def ventana_modificar_compra(self):
        # Validar que se haya seleccionado una compra
        self.compra_seleccionada = self.tree_lista_compras.focus()
        self.val_mod_compra = self.tree_lista_compras.item(self.compra_seleccionada, 'values')

        if self.val_mod_compra != '':
            self.frame_modificar_compra = Toplevel(self)
            self.frame_modificar_compra.title('Modificar Compra')
            self.frame_modificar_compra.geometry('500x300')
            self.frame_modificar_compra.resizable(0, 0)
            self.frame_modificar_compra.grab_set()

            lblframe_modificar_compra = LabelFrame(self.frame_modificar_compra)
            lblframe_modificar_compra.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

            lbl_codigo_modificar_compra = Label(lblframe_modificar_compra, text='Código Compra')
            lbl_codigo_modificar_compra.grid(row=0, column=0, padx=10, pady=10)
            self.txt_codigo_modificar_compra = Entry(lblframe_modificar_compra, width=40)
            self.txt_codigo_modificar_compra.grid(row=0, column=1, padx=10, pady=10)

            lbl_fecha_modificar_compra = Label(lblframe_modificar_compra, text='Fecha Compra')
            lbl_fecha_modificar_compra.grid(row=1, column=0, padx=10, pady=10)
            self.txt_fecha_modificar_compra = Entry(lblframe_modificar_compra, width=40)
            self.txt_fecha_modificar_compra.grid(row=1, column=1, padx=10, pady=10)

            lbl_total_modificar_compra = Label(lblframe_modificar_compra, text='Total Compra')
            lbl_total_modificar_compra.grid(row=2, column=0, padx=10, pady=10)
            self.txt_total_modificar_compra = Entry(lblframe_modificar_compra, width=40)
            self.txt_total_modificar_compra.grid(row=2, column=1, padx=10, pady=10)

            btn_guardar_modificar_compra = ttk.Button(lblframe_modificar_compra, text='Modificar', width=38,
                                                        command=self.modificar_compra)
            btn_guardar_modificar_compra.grid(row=4, column=1, padx=10, pady=10)
            self.llenar_entrys_modificar_compra()

            # Llamar a la función cargar_datos_compra para cargar los datos de la compra a modificar
            self.txt_fecha_modificar_compra.focus()

    def llenar_entrys_modificar_compra(self):
        # Limpiar todos los campos de entrada
        self.txt_codigo_modificar_compra.delete(0, END)
        self.txt_fecha_modificar_compra.delete(0, END)
        self.txt_total_modificar_compra.delete(0, END)

        # Llenar los campos de entrada con los datos de la compra seleccionada
        self.txt_codigo_modificar_compra.insert(0, self.val_mod_compra[0])
        self.txt_codigo_modificar_compra.config(state='readonly')
        self.txt_fecha_modificar_compra.insert(0, self.val_mod_compra[1])
        self.txt_total_modificar_compra.insert(0, self.val_mod_compra[2])

    def modificar_compra(self):
        # Validar que no queden campos vacíos
        if self.txt_codigo_modificar_compra.get() == "" or self.txt_fecha_modificar_compra.get() == "" or self.txt_total_modificar_compra.get() == "":
            messagebox.showwarning("Modificar Compra", "Por favor, complete todos los campos para modificar una compra.")
            return

        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            datos_modificar_compra = (
                self.txt_fecha_modificar_compra.get(),
                self.txt_total_modificar_compra.get()
            )

            # Consultar la base de datos para actualizar la compra
            miCursor.execute("UPDATE Compras SET Fecha=?,Total=? WHERE 'Codigo Compra'=" + self.txt_codigo_modificar_compra.get(), datos_modificar_compra)
            messagebox.showinfo('Modificar Compra', "Compra Modificada Correctamente")
            # Aplicar cambios
            miConexion.commit()
            # Actualizar la vista de la lista de compras
            self.val_mod_compra = (
                self.txt_fecha_modificar_compra.get(),
                self.txt_total_modificar_compra.get()
            )
            self.val_mod_compra = self.tree_lista_compras.item(self.compra_seleccionada, text='', values=
            (self.txt_codigo_modificar_compra.get(), self.txt_fecha_modificar_compra.get(),
            self.txt_total_modificar_compra.get()))
            self.frame_modificar_compra.destroy()  # Cerrar la ventana de modificación
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Modificar Compra", "Ocurrió un error al modificar la compra")

    def ventana_eliminar_compra(self):
        # Validar que se haya seleccionado una compra
        self.compra_seleccionada = self.tree_lista_compras.focus()
        self.val_elim_compra = self.tree_lista_compras.item(self.compra_seleccionada, 'values')

        if self.val_elim_compra != '':
            self.frame_eliminar_compra = Toplevel(self)
            self.frame_eliminar_compra.title('Eliminar Compra')
            self.frame_eliminar_compra.geometry('500x250')
            self.frame_eliminar_compra.resizable(0, 0)
            self.frame_eliminar_compra.grab_set()

            lblframe_eliminar_compra = LabelFrame(self.frame_eliminar_compra)
            lblframe_eliminar_compra.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

            lbl_confirmacion = Label(lblframe_eliminar_compra, text='¿Está seguro que desea eliminar esta compra?')
            lbl_confirmacion.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            lbl_codigo_compra = Label(lblframe_eliminar_compra, text='Código Compra:')
            lbl_codigo_compra.grid(row=1, column=0, padx=10, pady=10)
            lbl_codigo_compra_valor = Label(lblframe_eliminar_compra, text=self.val_elim_compra[0])
            lbl_codigo_compra_valor.grid(row=1, column=1, padx=10, pady=10)

            lbl_fecha_compra = Label(lblframe_eliminar_compra, text='Fecha Compra:')
            lbl_fecha_compra.grid(row=2, column=0, padx=10, pady=10)
            lbl_fecha_compra_valor = Label(lblframe_eliminar_compra, text=self.val_elim_compra[1])
            lbl_fecha_compra_valor.grid(row=2, column=1, padx=10, pady=10)

            lbl_total_compra = Label(lblframe_eliminar_compra, text='Total Compra:')
            lbl_total_compra.grid(row=3, column=0, padx=10, pady=10)
            lbl_total_compra_valor = Label(lblframe_eliminar_compra, text=self.val_elim_compra[2])
            lbl_total_compra_valor.grid(row=3, column=1, padx=10, pady=10)

            btn_eliminar_compra = ttk.Button(lblframe_eliminar_compra, text='Eliminar', width=38,
                                            style='danger', command=self.eliminar_compra)
            btn_eliminar_compra.grid(row=4, column=1, padx=10, pady=10)

    def eliminar_compra(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Obtener el código de la compra a eliminar
            codigo_compra = self.val_elim_compra[0]

            # Consultar la base de datos para eliminar la compra
            miCursor.execute("DELETE FROM Compras WHERE 'Codigo Compra'=?", (codigo_compra,))
            messagebox.showinfo('Eliminar Compra', 'Compra Eliminada Correctamente')
            # Aplicar cambios
            miConexion.commit()
            # Actualizar la vista de la lista de compras
            self.tree_lista_compras.delete(self.compra_seleccionada)
            self.frame_eliminar_compra.destroy()  # Cerrar la ventana de eliminación
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror('Eliminar Compra', 'Ocurrió un error al eliminar la compra')


#====================================
#============ REPORTES ==============
#====================================
    def ventana_lista_reportes(self):
        self.frame_lista_reportes = Frame(self.frame_center)
        self.frame_lista_reportes.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.lblframe_botones_listreportes = LabelFrame(self.frame_lista_reportes)
        self.lblframe_botones_listreportes.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        btn_generar_reporte = tb.Button(self.lblframe_botones_listreportes, text='Generar Reporte', width=15, bootstyle="success",command=self.ventana_generar_reporte)
        btn_generar_reporte.grid(row=0, column=0, padx=5, pady=5)

        btn_exportar_reporte = tb.Button(self.lblframe_botones_listreportes, text='Exportar Reporte', width=15, bootstyle="warning",command=self.ventana_exportar_reporte)
        btn_exportar_reporte.grid(row=0, column=1, padx=5, pady=5)

        btn_eliminar_reporte = tb.Button(self.lblframe_botones_listreportes, text='Eliminar Reporte', width=15, bootstyle="danger",command=self.ventana_eliminar_reporte)
        btn_eliminar_reporte.grid(row=0, column=2, padx=5, pady=5)

        self.lblframe_busqueda_listreportes = LabelFrame(self.frame_lista_reportes)
        self.lblframe_busqueda_listreportes.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        txt_busqueda_reportes = ttk.Entry(self.lblframe_busqueda_listreportes, width=73)
        txt_busqueda_reportes.grid(row=0, column=0, padx=5, pady=5)

        self.lblframe_tree_listreportes = LabelFrame(self.frame_lista_reportes)
        self.lblframe_tree_listreportes.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        columnas = ("codigo_reporte", "fecha", "tipo")

        self.tree_lista_reportes = tb.Treeview(self.lblframe_tree_listreportes, columns=columnas,
                                            height=17, show='headings', bootstyle='dark')
        self.tree_lista_reportes.grid(row=0, column=0)

        self.tree_lista_reportes.heading("codigo_reporte", text="Codigo Reporte", anchor=W)
        self.tree_lista_reportes.heading("fecha", text="Fecha", anchor=W)
        self.tree_lista_reportes.heading("tipo", text="Tipo", anchor=W)
        self.tree_lista_reportes['displaycolumns'] = ("codigo_reporte", "fecha", "tipo")

        # crear el scrollbar
        tree_scroll_listreportes = tb.Scrollbar(self.frame_lista_reportes, bootstyle="round-success")
        tree_scroll_listreportes.grid(row=2, column=1)

        # configurar el scrollbar
        tree_scroll_listreportes.config(command=self.tree_lista_reportes.yview)

        #Llamamos a nuestra funcion mostrar productos
        self.mostrar_reportes()

    def mostrar_reportes(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()
            # Limpiar el treeview de reportes
            registros = self.tree_lista_reportes.get_children()
            for elemento in registros:
                self.tree_lista_reportes.delete(elemento)
            # Consultar la base de datos para obtener los reportes
            miCursor.execute("SELECT * FROM Reportes")
            # Obtener los registros y guardarlos en "datos"
            datos = miCursor.fetchall()
            # Recorrer cada fila encontrada
            for row in datos:
                # Llenar el treeview con los datos de los reportes
                self.tree_lista_reportes.insert("", 0, text=row[0], values=(row[0], row[1], row[2]))
            # Aplicar cambios en la interfaz
            miConexion.commit()
            # Cerrar la conexión
            miConexion.close()
        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Lista de Reportes", "Ocurrió un error al mostrar la lista de reportes")

    def ventana_generar_reporte(self):
        self.frame_nuevo_reporte = Toplevel(self)
        self.frame_nuevo_reporte.title('Nuevo Reporte')
        self.frame_nuevo_reporte.geometry('510x300')
        self.frame_nuevo_reporte.resizable(0, 0)
        self.frame_nuevo_reporte.grab_set()

        lblframe_nuevo_reporte = LabelFrame(self.frame_nuevo_reporte)
        lblframe_nuevo_reporte.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        lbl_codigo_reporte = Label(lblframe_nuevo_reporte, text='Codigo Reporte')
        lbl_codigo_reporte.grid(row=0, column=0, padx=10, pady=10)
        self.txt_codigo_reporte = Entry(lblframe_nuevo_reporte, width=40)
        self.txt_codigo_reporte.grid(row=0, column=1, padx=10, pady=10)

        lbl_fecha_reporte = Label(lblframe_nuevo_reporte, text='Fecha Reporte')
        lbl_fecha_reporte.grid(row=1, column=0, padx=10, pady=10)
        self.txt_fecha_reporte = Entry(lblframe_nuevo_reporte, width=40)
        self.txt_fecha_reporte.grid(row=1, column=1, padx=10, pady=10)

        lbl_tipo_reporte = Label(lblframe_nuevo_reporte, text='Tipo Reporte')
        lbl_tipo_reporte.grid(row=2, column=0, padx=10, pady=10)
        self.txt_tipo_reporte = Entry(lblframe_nuevo_reporte, width=40)
        self.txt_tipo_reporte.grid(row=2, column=1, padx=10, pady=10)

        btn_generar_reporte = ttk.Button(lblframe_nuevo_reporte, text='Generar', width=38, command=self.guardar_reporte)
        btn_generar_reporte.grid(row=4, column=1, padx=10, pady=10)
        # Llamamos a la función ultimo_reporte
        self.ultimo_reporte()

    def guardar_reporte(self):
        # Validamos para que no queden vacíos los campos
        if self.txt_codigo_reporte.get() == "" or self.txt_fecha_reporte.get() == "" or self.txt_tipo_reporte.get() == "":
            messagebox.showwarning("Guardando Reporte", "Por favor, complete todos los campos para guardar un nuevo reporte.")
            return
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Obtener los datos del nuevo reporte
            datos_guardar_reporte = (
            self.txt_codigo_reporte.get(),
            self.txt_fecha_reporte.get(),
            self.txt_tipo_reporte.get()
            )

            # Consultar la base de datos para insertar el nuevo reporte
            miCursor.execute("INSERT INTO Reportes VALUES(?,?,?)", datos_guardar_reporte)
            messagebox.showinfo('Guardando Reporte', "Reporte Guardado Correctamente")
            # Aplicar cambios en la base de datos
            miConexion.commit()
            self.frame_nuevo_reporte.destroy()  # Cerramos la ventana
            self.ventana_lista_reportes()  # Cargamos la ventana para ver los cambios
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Guardando Reporte", "Ocurrió un error al guardar el reporte")

    def ultimo_reporte(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Consultar el máximo valor de CodigoReporte en Reportes
            miCursor.execute("SELECT MAX(`Codigo Reporte`) FROM Reportes")
            # Obtener el máximo valor
            codreporte = miCursor.fetchone()[0]

            # Si no hay registros o el máximo es None, establecer ultreporte a 1
            if codreporte is None:
                self.ultreporte = 1
            else:
                self.ultreporte = int(codreporte) + 1

            # Configurar el estado de txt_codigo_reporte
            self.txt_codigo_reporte.configure(state=NORMAL)
            self.txt_codigo_reporte.insert(0, self.ultreporte)
            self.txt_codigo_reporte.configure(state='readonly')

            # Aplicar cambios y cerrar la conexión
            miConexion.commit()
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Último Código de Reporte", "Ocurrió un error al obtener el último código de reporte")

    def ventana_exportar_reporte(self):
        # Validar que se haya seleccionado una compra
        self.reporte_seleccionada = self.tree_lista_reportes.focus()
        self.val_expo_reporte = self.tree_lista_reportes.item(self.reporte_seleccionada, 'values')
        self.frame_exportar_reporte = Toplevel(self)
        self.frame_exportar_reporte.title('Exportar Reporte')
        self.frame_exportar_reporte.geometry('400x150')
        self.frame_exportar_reporte.resizable(0, 0)
        self.frame_exportar_reporte.grab_set()

        lbl_confirmacion = Label(self.frame_exportar_reporte, text='¿Está seguro que desea exportar el reporte?')
        lbl_confirmacion.pack(pady=10)

        btn_exportar_reporte = Button(self.frame_exportar_reporte, text='Exportar', width=20,
                                          command=self.exportar_reporte)
        btn_exportar_reporte.pack(pady=10)

    def ventana_eliminar_reporte(self):
        # Validar que se haya seleccionado un reporte
        self.reporte_seleccionado = self.tree_lista_reportes.focus()
        self.val_elim_reporte = self.tree_lista_reportes.item(self.reporte_seleccionado, 'values')

        if self.val_elim_reporte != '':
            self.frame_eliminar_reporte = Toplevel(self)
            self.frame_eliminar_reporte.title('Eliminar Reporte')
            self.frame_eliminar_reporte.geometry('500x300')
            self.frame_eliminar_reporte.resizable(0, 0)
            self.frame_eliminar_reporte.grab_set()

            lblframe_eliminar_reporte = LabelFrame(self.frame_eliminar_reporte)
            lblframe_eliminar_reporte.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

            lbl_confirmacion = Label(lblframe_eliminar_reporte, text='¿Está seguro que desea eliminar este reporte?')
            lbl_confirmacion.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            lbl_codigo_reporte = Label(lblframe_eliminar_reporte, text='Código Reporte:')
            lbl_codigo_reporte.grid(row=1, column=0, padx=10, pady=10)
            lbl_codigo_reporte_valor = Label(lblframe_eliminar_reporte, text=self.val_elim_reporte[0])
            lbl_codigo_reporte_valor.grid(row=1, column=1, padx=10, pady=10)

            lbl_fecha_reporte = Label(lblframe_eliminar_reporte, text='Fecha Reporte:')
            lbl_fecha_reporte.grid(row=2, column=0, padx=10, pady=10)
            lbl_fecha_reporte_valor = Label(lblframe_eliminar_reporte, text=self.val_elim_reporte[1])
            lbl_fecha_reporte_valor.grid(row=2, column=1, padx=10, pady=10)

            lbl_tipo_reporte = Label(lblframe_eliminar_reporte, text='Tipo Reporte:')
            lbl_tipo_reporte.grid(row=3, column=0, padx=10, pady=10)
            lbl_tipo_reporte_valor = Label(lblframe_eliminar_reporte, text=self.val_elim_reporte[2])
            lbl_tipo_reporte_valor.grid(row=3, column=1, padx=10, pady=10)

            btn_eliminar_reporte = ttk.Button(lblframe_eliminar_reporte, text='Eliminar', width=38,
                                            style='danger', command=self.eliminar_reporte)
            btn_eliminar_reporte.grid(row=4, column=1, padx=10, pady=10)

    def eliminar_reporte(self):
        try:
            # Establecer la conexión
            miConexion = sqlite3.connect('Sispuntoventas.db')
            # Crear el cursor
            miCursor = miConexion.cursor()

            # Obtener el código del reporte a eliminar
            codigo_reporte = self.val_elim_reporte[0]

            # Consultar la base de datos para eliminar el reporte
            miCursor.execute("DELETE FROM Reportes WHERE 'Código Reporte'=?", (codigo_reporte,))
            messagebox.showinfo('Eliminar Reporte', 'Reporte Eliminado Correctamente')
            # Aplicar cambios
            miConexion.commit()
            # Actualizar la vista de la lista de reportes
            self.tree_lista_reportes.delete(self.reporte_seleccionado)
            self.frame_eliminar_reporte.destroy()  # Cerrar la ventana de eliminación
            # Cerrar la conexión
            miConexion.close()

        except Exception as e:
            print("Error:", e)
            messagebox.showerror('Eliminar Reporte', 'Ocurrió un error al eliminar el reporte')


    
#================================
#============ MAIN ==============
#================================
def main():
    app = Ventana()
    app.title('Sistema punto de ventas')
    app.state('zoomed')
    tb.Style('superhero')
    app.mainloop()

if __name__ == '__main__':
    main()
