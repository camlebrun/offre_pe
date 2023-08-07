import streamlit as st
import pandas as pd
import plotly.express as px

from pole_emploi_module import JobOffersModule

st.set_page_config(layout="wide")
st.title("Aidez-moi à trouver moi un nom de titre de page")


def main():
    col1, col2 = st.columns(2)
    with col1:
        rome = st.text_input("Entrez le code ROME :")
        rome_df = pd.read_csv("rome.csv")
        with st.expander("Voir les codes ROME"):
            st.dataframe(rome_df, use_container_width=True)

    with col2:
        region = st.text_input("Entrez le code de la région :")
        regions_df = pd.read_csv("regions.csv")
        with st.expander("Voir les codes régions"):
            st.dataframe(regions_df, use_container_width=True)

    if st.button("Obtenir les Offres d'Emploi"):
        try:
            module = JobOffersModule()
            offres_emploi = module.fetch_job_offers(rome, region)

            if not offres_emploi:
                st.warning("Aucune offre d'emploi trouvée.")
            else:
                st.success(f"{len(offres_emploi)} offres d'emploi trouvées.")
                if len(offres_emploi) == 3000:
                    st.warning("L'API ne renvoie que 3000 offres d'emploi.")

                data = []
                for offre in offres_emploi:
                    data.append(
                        {
                            "ID": offre.get("id", ""),
                            "Nom de l'entreprise": offre["entreprise"].get("nom", ""),
                            "Appellation": offre.get("appellationlibelle", ""),
                            "Lieu": offre["lieuTravail"].get("libelle", ""),
                            "Type de Contrat": offre.get("typeContrat", ""),
                            "Nombre de Postes": offre.get("nombrePostes", ""),
                        }
                    )

                df = pd.DataFrame(data)
                df.reset_index(drop=True, inplace=True)  # Réinitialiser l'index
                col1, col2 = st.columns(2)

                with col1:
                    st.write("Agrégation par nombre de postes proposé dans l'annonce:")
                    aggregate_par_positions = (
                        df.groupby("Nombre de Postes")
                        .size()
                        .reset_index(name="Count")
                        .sort_values(by="Count", ascending=False)
                        .reset_index(drop=True)
                    )
                    total_count = aggregate_par_positions["Count"].sum()
                    aggregate_par_positions["Percentage"] = (
                        round((aggregate_par_positions["Count"] / total_count), 3) * 100
                    )
                    st.dataframe(aggregate_par_positions, use_container_width=True)

                    st.write("Agrégation par lieu :")
                    aggregate_par_lieu = (
                        df.groupby("Lieu")
                        .size()
                        .reset_index(name="Count")
                        .sort_values(by="Count", ascending=False)
                        .reset_index(drop=True)
                    )
                    total_count = aggregate_par_lieu["Count"].sum()
                    aggregate_par_lieu["Percentage"] = (
                        round((aggregate_par_lieu["Count"] / total_count), 3) * 100
                    )
                    total_count = aggregate_par_lieu["Count"].sum()
                    aggregate_par_lieu["Percentage"] = (
                        round((aggregate_par_lieu["Count"] / total_count), 3) * 100
                    )
                    st.dataframe(aggregate_par_lieu, use_container_width=True)

                with col2:
                    st.write("Agrégation par Type de contrat :")
                    aggregate_par_contrat = (
                        df.groupby("Type de Contrat")
                        .size()
                        .reset_index(name="Count")
                        .sort_values(by="Count", ascending=False)
                        .reset_index(drop=True)
                    )
                    fig = px.pie(
                        aggregate_par_contrat,
                        values="Count",
                        names="Type de Contrat",
                        title="Répartition par type de contrat",
                    )
                    st.plotly_chart(fig, use_container_width=True)
                   # st.dataframe(aggregate_par_contrat, use_container_width=True)

                    st.write("Agrégation par nom de l'entreprise :")
                    aggregate_par_entreprise = (
                        df.groupby("Nom de l'entreprise")
                        .size()
                        .reset_index(name="Count")
                        .sort_values(by="Count", ascending=False)
                        .reset_index(drop=True)
                    )
                    total_count = aggregate_par_entreprise["Count"].sum()
                    aggregate_par_entreprise["Percentage"] = (
                        round((aggregate_par_entreprise["Count"] / total_count), 3)
                        * 100
                    )

                    st.dataframe(aggregate_par_entreprise, use_container_width=True)

                st.write(
                    "Les codes ROME englobent des métiers proches, pour plus d'informations sur les offres d'emplois vous pouvez consulter le tableau ci-dessous."
                )
                st.write("Agrégation par nom de métiers :")
                aggregate_par_appellation = (
                    df.groupby("Appellation")
                    .size()
                    .reset_index(name="Count")
                    .sort_values(by="Count", ascending=False)
                    .reset_index(drop=True)
                )
                aggregate_par_appellation.columns = ["Appellation", "Count"]
                total_count = aggregate_par_appellation["Count"].sum()
                aggregate_par_appellation["Percentage"] = (
                    round((aggregate_par_appellation["Count"] / total_count), 3) * 100
                )

                st.dataframe(aggregate_par_appellation, use_container_width=True)

        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")


if __name__ == "__main__":
    main()
