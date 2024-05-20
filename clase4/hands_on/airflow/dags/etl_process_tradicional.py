#Es un poco diferente al del profe
import datetime

import pandas as pd

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from ucimlrepo import fetch_ucirepo

# Podemos cambiar los argumentos por defecto
default_args = {
    'depends_on_past': False,
    'schedule_interval': None, #intevalos
    'retries': 1, #reintentos
    'retry_delay': datetime.timedelta(minutes=5), #el delay para reintentar, para darle el tiempo de que termine otro proceso
    'dagrun_timeout': datetime.timedelta(minutes=15) #si nuestro proceso tarda más, lo mata
}

# Creamos el objeto DAG
dag = DAG(
    'etl_without_taskflow', # ID del dag que va a usar en la IU
    default_args=default_args, # Le mandamos valores por defecto
    description='Proceso ETL de ejemplo sin TaskFlow', #Se puede agregar una descripción
    schedule_interval=None, # Se le puede configurar otra vez el intervalo, y hay cosas que funcionan mejor configurando acá abajo u otras veces arriba
    start_date=days_ago(2), #Fecha de incio del dag, se usa para programar que corra semanalmente, espera que transcurra una semana de su fecha de incio para volver a correr
    # Entonces si se corta la luz, y se pierde una hora fijada, lo corre en cuando se encienda, es más robusto
    tags=['ETL'] 
)

def obtain_original_data(): #Funciones que corren dentro del DAG.
    """
    Carga los datos desde de la fuente
    """
    # Obtenemos el dataset
    heart_disease = fetch_ucirepo(id=45)
    dataframe = heart_disease.data.original
    # Todos valores mayores a cero es una enfermedad cardiaca
    dataframe.loc[dataframe["num"] > 0, "num"] = 1
    path = "./data.csv"
    dataframe.to_csv(path, index=False)

    # Enviamos un mensaje para el siguiente nodo
    return path #Todo lo de return va a un canal de comunicación de tareas que se llama xcom. Cualquier tarea puede leer lo de xcom


def make_dummies_variables(**kwargs):
    """
    Convierte a las variables en Dummies
    """
    ti = kwargs['ti'] #Es el entonrno donde está trabajando Airflow. Se puede agregar el ti como argumento en vez de acá y no poner nada cunado se lo llame
    path_input = ti.xcom_pull(task_ids='obtain_original_data') #ti tien el xcom. Con xcom_pull quiero traer la información que dejó la funición de arriba
    #Con xcom_push le podemos dar el nombre a la variable, 
    a = 0
    b = 0

    if path_input:

        # Limpiamos duplicados
        dataset = pd.read_csv(path_input) #Mandamos solo el path porque xcom está pensado para mandar varaibles pequeñas y no datasets, solo el path se manda

        # Y quitamos nulos
        dataset.drop_duplicates(inplace=True, ignore_index=True)
        dataset.dropna(inplace=True, ignore_index=True)

        # Forzamos las categorias en las columnas
        dataset["cp"] = dataset["cp"].astype(int)
        dataset["restecg"] = dataset["restecg"].astype(int)
        dataset["slope"] = dataset["slope"].astype(int)
        dataset["ca"] = dataset["ca"].astype(int)
        dataset["thal"] = dataset["thal"].astype(int)

        categories_list = ["cp", "restecg", "slope", "ca", "thal"]
        dataset_with_dummies = pd.get_dummies(data=dataset, columns=categories_list, drop_first=True)
        dataset_with_dummies.to_csv("./data_clean_dummies.csv", index=False)

        # Enviamos dos mensajes entre nodo
        # OBS: Recordad que no se mandan mucha información, solo mensajes de comunicación. Si querés pasar dataset
        # entre nodos, es mejor guardar en algún lado y pasar el path o similar.
        a = dataset_with_dummies.shape[0]
        b = dataset_with_dummies.shape[1]

    return {"observations": a, "columns": b} #Devuelve un dic


def split_dataset(**kwargs): #Divide el dataset, 
    """
    Genera el dataset y obtiene set de testeo y evaluación
    """
    ti = kwargs['ti']
    # Leemos el mensaje del DAG anterior
    dummies_output = ti.xcom_pull(task_ids='make_dummies_variables')

    dataset = pd.read_csv("./data_clean_dummies.csv")

    if dataset.shape[0] == dummies_output["observations"] and dataset.shape[1] == dummies_output["columns"]:

        X = dataset.drop(columns="num")
        y = dataset[["num"]]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)

        #Los graba para que la siguiente tarea lo pueda ver
        X_train.to_csv("./X_train.csv", index=False)
        X_test.to_csv("./X_test.csv", index=False)
        y_train.to_csv("./y_train.csv", index=False)
        y_test.to_csv("./y_test.csv", index=False)

def normalize_data():
    """
    Estandarizamos los datos
    """
    X_train = pd.read_csv("./X_train.csv")
    X_test = pd.read_csv("./X_test.csv")

    #Normaliza
    sc_X = StandardScaler(with_mean=True, with_std=True)
    X_train_arr = sc_X.fit_transform(X_train)
    X_test_arr = sc_X.transform(X_test)

    X_train = pd.DataFrame(X_train_arr, columns=X_train.columns)
    X_test = pd.DataFrame(X_test_arr, columns=X_test.columns)

    #Los vuelve a guardar
    X_train.to_csv("./X_train.csv", index=False)
    X_test.to_csv("./X_test.csv", index=False)

def read_train_data():
    """
    Leemos los datos de entrenamiento
    """
    X_train = pd.read_csv("./X_train.csv")
    y_train = pd.read_csv("./y_train.csv")
    print(f"Las X de entrenamiento son {X_train.shape} y las y son {y_train.shape}")

def read_test_data():
    """
    Leemos los datos de testeo
    """
    X_test = pd.read_csv("./X_test.csv")
    y_test = pd.read_csv("./y_test.csv")
    print(f"Las X de testeo son {X_test.shape} y las y son {y_test.shape}")

#Hemos definido funciones pero podrían ser clases

#Las tareas las genera con un operador
obtain_original_data_operator = PythonOperator(
    task_id='obtain_original_data', #Le damos el ID de la tarea
    python_callable=obtain_original_data, #La función que va a llamar, puede tener el mismo nombre para no confundirse
    dag=dag #Le decimos el dag
)

make_dummies_variables_operator = PythonOperator(
    task_id='make_dummies_variables',
    provide_context=True,
    python_callable=make_dummies_variables,
    dag=dag
)

split_dataset_operator = PythonOperator(
    task_id='split_dataset',
    provide_context=True,
    python_callable=split_dataset,
    dag=dag
)

normalize_data_operator = PythonOperator(
    task_id='normalize_data',
    python_callable=normalize_data,
    dag=dag
)

read_train_data_operator = PythonOperator(
    task_id='read_train_data',
    python_callable=read_train_data,
    dag=dag
)

read_test_data_operator = PythonOperator(
    task_id='read_test_data',
    python_callable=read_test_data,
    dag=dag
)
#Lo que seguiría sería
#Busqueda de hiperparámetros
#Selección de modelos 
#Etc.

#Una vez tenemos las tareas, se le debe indicar el orden, con las flechitas >>
obtain_original_data_operator >> make_dummies_variables_operator >> split_dataset_operator >> normalize_data_operator
normalize_data_operator >> [read_train_data_operator, read_test_data_operator] #La lista significa que las tareas corren en paralelo.

#Airflow no muestra imágenes porque no se muestra el proceso, sino que debería almacenar por código

