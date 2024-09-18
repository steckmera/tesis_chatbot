# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg
#
#
class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hola_mundo"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         con = psycopg.connect(dbname="chatbot", host="localhost", user="postgres", password="123456", port="5432")
         cur = con.cursor()
         cur.execute("SELECT value FROM info WHERE code = 'requisitos_admisiones'")
         res = cur.fetchone()

         value = res[0]

         cur.close()
         con.close()


         dispatcher.utter_message(text=value)

         return []

class ActionInfoAdmisiones(Action):

     def name(self) -> Text:
         return "action_informacion_admisiones"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         con = psycopg.connect(dbname="chatbot", host="localhost", user="postgres", password="123456", port="5432")
         cur = con.cursor()
         cur.execute("SELECT value FROM info WHERE code = 'informacion_admisiones'")
         res = cur.fetchone()

         value = res[0]

         cur.close()
         con.close()


         dispatcher.utter_message(text=value)

         return []

class ActionValoresAdmisiones(Action):

     def name(self) -> Text:
         return "action_valores_admisiones"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         con = psycopg.connect(dbname="chatbot", host="localhost", user="postgres", password="123456", port="5432")
         cur = con.cursor()
         cur.execute("SELECT value FROM info WHERE code = 'valores_admisiones'")
         res = cur.fetchone()

         value = res[0]

         cur.close()
         con.close()


         dispatcher.utter_message(text=value)

         return []

class ActionRequisitosAdmisiones(Action):

     def name(self) -> Text:
         return "action_requisitos_admisiones"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         con = psycopg.connect(dbname="chatbot", host="localhost", user="postgres", password="123456", port="5432")
         cur = con.cursor()
         cur.execute("SELECT value FROM info WHERE code = 'requisitos_admisiones'")
         res = cur.fetchone()

         value = res[0]

         cur.close()
         con.close()


         dispatcher.utter_message(text=value)

         return []

class ActionHorariosAdministracion(Action):

     def name(self) -> Text:
         return "action_horarios_administracion"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         con = psycopg.connect(dbname="chatbot", host="localhost", user="postgres", password="123456", port="5432")
         cur = con.cursor()
         cur.execute("SELECT value FROM info WHERE code = 'horarios_administracion'")
         res = cur.fetchone()

         value = res[0]

         cur.close()
         con.close()

         dispatcher.utter_message(text=value)

         return []

class ActionPagosAdministracion(Action):

     def name(self) -> Text:
         return "action_pagos_administracion"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         con = psycopg.connect(dbname="chatbot", host="localhost", user="postgres", password="123456", port="5432")
         cur = con.cursor()
         cur.execute("SELECT value FROM info WHERE code = 'pagos_administracion'")
         res = cur.fetchone()

         value = res[0]

         cur.close()
         con.close()


         dispatcher.utter_message(text=value)

         return []

class ActionTransportAdministracion(Action):

     def name(self) -> Text:
         return "action_transporte_administracion"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         con = psycopg.connect(dbname="chatbot", host="localhost", user="postgres", password="123456", port="5432")
         cur = con.cursor()
         cur.execute("SELECT value FROM info WHERE code = 'transporte_administracion'")
         res = cur.fetchone()

         value = res[0]

         cur.close()
         con.close()


         dispatcher.utter_message(text=value)

         return []