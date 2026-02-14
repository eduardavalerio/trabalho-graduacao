import os
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import cartopy.crs as ccrs

#diretorio com os files .mat
diret  = '/Volumes/LAGEM/isas-data/'
anos = range(2002, 2021)  # 2002 a 2020
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
         'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

for ano in anos:
    path = os.path.join(diret, f'{ano}.mat')
        
    print(f"Processando ano: {ano}...")
    data = loadmat(path)
    
    #variables
    temp = data['temp'] #temperatura
    pv = data['pv'] #vorticidade potencial
    salt = data['salt'] #salinidade
    lat = data['lat'] #lat
    lon = data['lon'] #long
    pp = data['pp'] #profundidade 

    
    # Máscaras booleanas para os três tipos de AMSTAS seguindo os parâmetros de Sato & Polito, 2014.
    pv_mask = pv <= 1.5e-10 # é o mesmo para todos os tipos 
    amstas1 = ((temp >= 14.1) & (temp <= 15.9)) & ((salt >= 35.4) & (salt <= 35.8)) & pv_mask
    amstas2 = ((temp >= 15.8) & (temp <= 17.6)) & ((salt >= 35.5) & (salt <= 35.9)) & pv_mask
    amstas3 = ((temp >= 12.3) & (temp <= 14.1)) & ((salt >= 35.0) & (salt <= 35.4)) & pv_mask

    # Plotar imagem
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(15, 18),
                             subplot_kw={'projection': ccrs.PlateCarree()})
    axes_flat = axes.flatten()

    #loop para plotar cada mês
    for i in range(12):
        ax = axes_flat[i]
    
        #superficie
        sup1 = amstas1[:,:,0,i].astype(float)
        sup1[sup1==0] = np.nan #só plota o que for true da máscara booleana amstas1
        sup2 = amstas2[:,:,0,i].astype(float)
        sup2[sup2==0] = np.nan
        sup3 = amstas3[:,:,0,i].astype(float)
        sup3[sup3==0] = np.nan

        #mapa
        ax.set_extent([-60, 20, -60, -20], crs=ccrs.PlateCarree()) #recorte do mapa
        ax.add_feature(cfeature.LAND, facecolor='lightgray') #cor do continente
        ax.add_feature(cfeature.OCEAN, facecolor='white') #cor oceano
        ax.coastlines(resolution='50m', linewidth=0.5) #linha de costa 
    
        # Plotar a presença
        mesh1 = ax.pcolormesh(lon.flatten(), lat.flatten(), sup1.T, 
                              transform=ccrs.PlateCarree(),
                              cmap='winter', vmin=0, vmax=1)
        mesh2 = ax.pcolormesh(lon.flatten(), lat.flatten(), sup2.T, 
                              transform=ccrs.PlateCarree(),
                              cmap='plasma_r', vmin=0, vmax=1)

        mesh3 =  ax.pcolormesh(lon.flatten(), lat.flatten(), sup3.T, 
                              transform=ccrs.PlateCarree(),
                              cmap='Wistia', vmin=0, vmax=1)

        ax.set_title({meses[i]}, fontsize=12)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle(f'AMSTAS (Superfície) {ano}', fontsize=22)
    
    plt.savefig(f'amstas{ano}.png', dpi=150)
    plt.close(fig)
    print(f"Salvo: amstas{ano}.png")

print("Processamento concluído!")

