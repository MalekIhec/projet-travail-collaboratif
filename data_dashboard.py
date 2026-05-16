#!/usr/bin/env python
# coding: utf-8

# In[39]:


import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
df_clients = pd.read_csv('clients_data.csv')
df_ventes = pd.read_csv('ventes_data.csv')


# In[40]:


print(f"Lignes et colonnes ventes : {df_ventes.shape}")
print(f"Lignes et colonnes clients : {df_clients.shape}")


# In[41]:


df_clients.describe()


# In[42]:


df_ventes.describe()


# In[43]:


df_clients.describe(include=["object"])


# In[44]:


df_ventes.describe(include=["object"])


# In[45]:

# Créer une colonne date
df_ventes['date_transaction'] = pd.to_datetime(df_ventes['date_transaction'])
df_ventes['mois'] = df_ventes['date_transaction'].dt.month
df_ventes['année'] = df_ventes['date_transaction'].dt.year

print("Colonne date ajoutée !")
print(df_ventes.head())

df_clients.isnull().sum()


# In[46]:


df_clients=df_clients.drop(columns=["telephone"])
df_clients


# In[47]:


df_clients["age"]=df_clients['age'].fillna(df_clients['age'].median())
df_clients


# In[48]:


df_ventes["prix_unitaire"]=df_ventes['prix_unitaire'].fillna(df_ventes['prix_unitaire'].mean())
df_ventes


# In[49]:


df_ventes['paiement'] = df_ventes['paiement'].fillna('Inconnu')
df_ventes


# In[50]:


df_ventes = df_ventes.drop_duplicates()


# In[51]:


print("Le nettoyage du DataFrame ventes est terminé ! Valeurs manquantes restantes :", 
df_ventes.isnull().sum().sum())


# In[52]:


print("Le nettoyage du DataFrame clients est terminé ! Valeurs manquantes restantes :", 
df_clients.isnull().sum().sum())


# In[53]:


df_clients["ville"].value_counts()


# In[54]:


df_ventes["produit"].value_counts()


# In[55]:


df_ventes["produit"].unique()


# In[56]:


df_clients[(df_clients["ville"]=="Tunis") & (df_clients["age"]>25)]


# In[57]:


df_ventes.sort_values(by="prix_unitaire",ascending=False)



# Analyser les clients par revenu
revenu_par_client = df_final.groupby('Customer_Name').agg({
    'Revenue': 'sum',
    'Quantity': 'sum',
    'Age': 'first'
}).sort_values('Revenue', ascending=False)

st.subheader("🏆 Top 10 Clients")
st.dataframe(revenu_par_client.head(10))

# In[58]:


df_ventes.groupby("produit")["prix_unitaire"].mean()


# In[59]:


df_ventes['Revenu']=df_ventes['quantite'] * df_ventes['prix_unitaire']


# In[60]:


df_final=pd.merge(df_ventes, df_clients, on='client_id', how='inner')


# In[61]:


df_final.rename(columns={
    'transaction_id': 'Transaction_ID',
    'client_id': 'Client_ID',
    'produit': 'Product_Name',
    'quantite': 'Quantity',
    'prix_unitaire': 'Unit_Price',
    'paiement': 'Payment_Method',
    'Revenu': 'Revenue',
    'nom_client': 'Customer_Name',
    'age': 'Age',
    'ville': 'City'
}, inplace=True)
st.write(df_final.head())


# In[62]:


Product_Revenue = df_final.groupby('Product_Name')['Revenue'].sum()
Product_Revenue


# In[63]:


plt.bar(df_final["City"], df_final["Revenue"])
plt.xlabel("CITY")
plt.ylabel("VENTES")
plt.title("graphe de Ventes de chaque ville")
plt.show()


# In[64]:


df2=df_final.groupby("Product_Name")["Revenue"].sum()
plt.pie(df2,labels=df2.index,autopct="%1.1f%%")
plt.show()


# In[65]:


df2.plot(kind='bar')
plt.xticks(rotation=45)


# In[66]:


st.title ("Data Dashboard")


# In[67]:


st.write(df_final)


# # Dashboard Interactif Streamlit

# In[68]:


st.set_page_config(page_title="Dashboard Ventes", layout="wide")
st.title("📊 Data Dashboard")


# In[69]:


st.sidebar.header("🔍 Filtres")

villes = ['Toutes'] + list(df_final['City'].unique())
ville_selectionnee = st.sidebar.selectbox('Filtrer par Ville:', villes)

produits = ['Tous'] + list(df_final['Product_Name'].unique())
produit_selectionne = st.sidebar.selectbox('Filtrer par Produit:', produits)

paiements = ['Tous'] + list(df_final['Payment_Method'].unique())
paiement_selectionne = st.sidebar.selectbox('Filtrer par Mode de Paiement:', paiements)

age_min, age_max = int(df_final['Age'].min()), int(df_final['Age'].max())
age_range = st.sidebar.slider('Tranche d\'âge:', age_min, age_max, (age_min, age_max))


# In[70]:


df_filtre = df_final.copy()
if ville_selectionnee != 'Toutes':
    df_filtre = df_filtre[df_filtre['City'] == ville_selectionnee]
if produit_selectionne != 'Tous':
    df_filtre = df_filtre[df_filtre['Product_Name'] == produit_selectionne]
if paiement_selectionne != 'Tous':
    df_filtre = df_filtre[df_filtre['Payment_Method'] == paiement_selectionne]
df_filtre = df_filtre[(df_filtre['Age'] >= age_range[0]) & (df_filtre['Age'] <= age_range[1])]
df_filtre = df_filtre.copy()
df_filtre['Unit_Price'] = df_filtre['Unit_Price'].round(2)
df_filtre['Revenue'] = df_filtre['Revenue'].round(2)
df_filtre = df_filtre.copy()
df_filtre['Unit_Price'] = df_filtre['Unit_Price'].round(2)
df_filtre['Revenue'] = df_filtre['Revenue'].round(2)


# In[71]:


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Nombre de transactions", len(df_filtre))
with col2:
    st.metric("Revenu total", f"{df_filtre['Revenue'].sum():.2f}€")
with col3:
    st.metric("Revenu moyen", f"{df_filtre['Revenue'].mean():.2f}€")
with col4:
    st.metric("Satisfaction moyenne", f"{df_filtre['satisfaction'].mean():.2f}/5")


# In[72]:


tab1, tab2, tab3 = st.tabs(["📊 Graphiques", "📋 Données", "📈 Statistiques"])


# In[73]:


with tab1:
    if len(df_filtre) == 0:
        st.warning("⚠️ Aucune donnée pour ces filtres. Essaie une autre combinaison.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Revenu par Ville")
            fig, ax = plt.subplots(figsize=(8, 5))
            df_filtre.groupby('City')['Revenue'].sum().sort_values(ascending=False).plot(kind='bar', ax=ax, color='steelblue')
            ax.set_xlabel('Ville')
            ax.set_ylabel('Revenu')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.subheader("Revenu par Produit (%)")
            fig, ax = plt.subplots(figsize=(8, 5))
            df2 = df_filtre.groupby('Product_Name')['Revenue'].sum()
            ax.pie(df2, labels=df2.index, autopct='%1.1f%%')
            st.pyplot(fig)

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Revenu par Produit")
            fig, ax = plt.subplots(figsize=(8, 5))
            df_filtre.groupby('Product_Name')['Revenue'].sum().plot(kind='bar', ax=ax, color='coral')
            ax.set_xlabel('Produit')
            ax.set_ylabel('Revenu')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col4:
            st.subheader("Satisfaction par Produit")
            fig, ax = plt.subplots(figsize=(8, 5))
            df_filtre.groupby('Product_Name')['satisfaction'].mean().plot(kind='bar', ax=ax, color='green')
            ax.set_xlabel('Produit')
            ax.set_ylabel('Satisfaction moyenne')
            ax.set_ylim(0, 5)
            plt.xticks(rotation=45)
            st.pyplot(fig)


# In[74]:


with tab2:
    st.subheader("Données filtrées")
    st.write(f"Total lignes : {len(df_filtre)}")
    st.dataframe(df_filtre, use_container_width=True)
    csv = df_filtre.to_csv(index=False)
    st.download_button("📥 Télécharger les données", data=csv, file_name="donnees_filtrees.csv", mime="text/csv")


# In[75]:


with tab3:
    st.subheader("Statistiques Descriptives")
    st.write(df_filtre.drop(columns=["Transaction_ID", "Client_ID"]).describe())


# ## Conversion en script

# In[76]:



