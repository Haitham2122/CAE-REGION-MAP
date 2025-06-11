




def calculer_ae_total(data,G, FP):
    """
    Calcule l'économie annuelle d'énergie finale (AE) en kWh/an pour différents éléments de l'enveloppe 
    et retourne l'AE total.
    
    :param data: Dictionnaire contenant les surfaces et les coefficients U initiaux pour les différents éléments de l'enveloppe
    :param G: Coefficient selon la zone climatique (mille heures·K/an)
    :param FP: Facteur de pondération
    :return: Économie annuelle d'énergie finale totale (kWh/an)
    """
    # Extraction des valeurs du dictionnaire
    surface_murs_ext = 1
    surface_murs_non_chauffe = 1
    surface_planchers_bas =1
    surface_planchers_non_chauffe = 1
    surface_planchers_hauts = 1
    surface_toitures = 1

    U_initial_murs_ext = float(data["U_initial_murs_ext"])
    U_initial_murs_non_chauffe = float(data["U_initial_murs_non_chauffe"])
    U_initial_planchers_bas = float(data["U_initial_planchers_bas"])
    U_initial_planchers_non_chauffe = float(data["U_initial_planchers_non_chauffe"])
    U_initial_planchers_hauts = float(data["U_initial_planchers_hauts"])
    U_initial_toitures = float(data["U_initial_toitures"])

    # Dictionnaire des valeurs K_f pour les différents éléments de l'enveloppe
    valeurs_K_f = {
        "Murs extérieurs": 1/3.7,
        "Murs sur local non chauffé": 1/3.7,
        "Planchers bas": 1/3,
        "Planchers bas sur local non chauffé": 1/3.7,
        "Planchers hauts": 1/7,
        "Toitures": 1/6
    }
    
    # Calcul de l'AE pour chaque élément
    print(FP,(U_initial_murs_ext - valeurs_K_f["Murs extérieurs"]),G)
    AE_murs_ext = FP * (U_initial_murs_ext - valeurs_K_f["Murs extérieurs"]) * surface_murs_ext * G
    AE_murs_non_chauffe = FP * (U_initial_murs_non_chauffe - valeurs_K_f["Murs sur local non chauffé"]) * surface_murs_non_chauffe * G
    AE_planchers_bas = FP * (U_initial_planchers_bas - valeurs_K_f["Planchers bas"]) * surface_planchers_bas * G
    AE_planchers_non_chauffe = FP * (U_initial_planchers_non_chauffe - valeurs_K_f["Planchers bas sur local non chauffé"]) * surface_planchers_non_chauffe * G
    AE_planchers_hauts = FP * (U_initial_planchers_hauts - valeurs_K_f["Planchers hauts"]) * surface_planchers_hauts * G
    AE_toitures = FP * (U_initial_toitures - valeurs_K_f["Toitures"]) * surface_toitures * G
    
 
    
    return {"Murs extérieurs":round(AE_murs_ext,2), "Murs sur local non chauffé":round(AE_murs_non_chauffe,2) ,"Planchers bas": round(AE_planchers_bas,2) ,"Planchers bas sur local non chauffé":round(AE_planchers_non_chauffe,2) , "Planchers hauts":round(AE_planchers_hauts,2) , "Toitures":round(AE_toitures,2)}



def obtenir_coefficient_G(province, zone):
    zone_climatique_hiver=zone[0]
    zone_climatique_ete=zone[1]
    # Coefficients pour les îles Baléares, Ceuta et Melilla
    coefficients_peninsulaires = {
        ('C', '1'): 44, ('D', '1'): 60, ('E', '1'): 74,
        ('C', '2'): 45, ('D', '2'): 60,
        ('A', '3'): 25, ('B', '3'): 32, ('C', '3'): 46, ('D', '3'): 61,
        ('A', '4'): 26, ('B', '4'): 33, ('C', '4'): 46,
    }
    
    # Coefficients pour les Canaries
    coefficients_canaries = {
        ('A', '2'): 20, ('B', '2'): 30, ('C', '2'): 42,
    }

    # Définir les provinces appartenant aux Canaries
    provinces_canaries = ["Palmas, Las", "Santa Cruz de Tenerife"]

    # Vérifier la province et retourner le coefficient G correspondant
    if province in provinces_canaries:
        key = (zone_climatique_hiver, zone_climatique_ete)
        return coefficients_canaries.get(key, "Zone climatique non définie pour cette combinaison.")
    else:
        key = (zone_climatique_hiver, zone_climatique_ete)
        return coefficients_peninsulaires.get(key, "Zone climatique non définie pour cette combinaison.")

# Exemple d'utilisation
def get_zone(province, altitude):
    """
    Determine the zone for a given province and altitude using the zone_data_list_full.

    Args:
    province (str): The name of the province.
    altitude (int): The altitude to check.

    Returns:
    str: The zone corresponding to the given province and altitude.
    """
    altitude=float(altitude.replace(" ","").replace("m",""))
    if province not in zone_data_list_full:
        return "Province not found"

    # Altitude ranges as defined in the original table: [0, 50, 100, ..., 1250, >=1300]
    altitude_ranges = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1250, 1300]

    for i, alt_range in enumerate(altitude_ranges):
        if altitude <= alt_range:
            return zone_data_list_full[province][i]

    # If altitude is greater than the highest range, return the last zone
    return zone_data_list_full[province][-1]
zone_data_list_full = {
    'Albacete': ['C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Alicante/Alacant': ['B4', 'B4', 'B4', 'B4', 'B4', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3'],
    'Almería': ['A4', 'A4', 'B4', 'B4', 'B4', 'B3', 'B3', 'B3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3'],
    'Araba/Álava': ['D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Asturias': ['C1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Ávila': ['D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Badajoz': ['C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3'],
    'Balears, Illes': ['B3', 'B3', 'B3', 'B3', 'B3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3'],
    'Barcelona': ['C2', 'C2', 'C2', 'C2', 'C2', 'D2', 'D2', 'D2', 'D2', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Bizkaia': ['C1', 'C1', 'C1', 'C1', 'C1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1'],
    'Burgos': ['D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Cáceres': ['C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3'],
    'Cádiz': ['A3', 'A3', 'A3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E1', 'E1', 'E1'],
    'Cantabria': ['C1', 'C1', 'C1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Castellón/Castelló': ['B3', 'B3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2'],
    'Ceuta': ['B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3'],
    'Ciudad Real': ['C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3'],
    'Córdoba': ['B4', 'B4', 'B4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3'],
    'Coruña, A': ['C1', 'C1', 'C1', 'C1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Cuenca': ['D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Gipuzkoa': ['D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Girona': ['C2', 'C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Granada': ['A4', 'A4', 'B4', 'B4', 'B4', 'B3', 'B3', 'B3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3'],
    'Guadalajara': ['D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Huelva': ['D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Huesca': ['E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Jaén': ['D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'León': ['E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Lleida': ['E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Lugo': ['E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Madrid': ['D3', 'D3', 'D2', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Málaga': ['D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3'],
    'Melilla': ['A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3', 'A3'],
    'Murcia': ['D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3'],
    'Navarra': ['E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Ourense': ['E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Palencia': ['E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Palmas, Las': ['B2', 'B2', 'B2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2'],
    'Pontevedra': ['D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'D1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Rioja, La': ['E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Salamanca': ['E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Santa Cruz de Tenerife': ['B2', 'B2', 'B2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2'],
    'Segovia': ['D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Sevilla': ['B4', 'B4', 'B4', 'B4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4'],
    'Soria': ['D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Tarragona': ['B3', 'B3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3'],
    'Teruel': ['C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E1', 'E1', 'E1', 'E1'],
    'Toledo': ['C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3'],
    'Valencia/València': ['B3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'C3', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Valladolid': ['D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Zamora': ['D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1', 'E1'],
    'Zaragoza': ['C3', 'C3', 'C3', 'C3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'D3', 'E1', 'E1', 'E1', 'E1']
}
