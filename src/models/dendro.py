from enum import Enum
from typing import Set, Optional

from pydantic import BaseModel, Field
from .measurement import Measurement


class Taxon(str, Enum):
    Abies_alba = 'Abies alba Mill.'
    Acer_campestre = 'Acer campestre L.'
    Acer_platanoides = 'Acer platanoides L.'
    Acer_pseudoplatanus = 'Acer pseudoplatanus L.'
    Aesculus_hippocastanum = 'Aesculus hippocastanum L.'
    Alnus_glutinosa = 'Alnus glutinosa Gaertn.'
    Alnus_incana = 'Alnus incana DC.'
    Alnus_viridis = 'Alnus viridis DC.'
    Amelanchier_ovalis = 'Amelanchier ovalis Med.'
    Berberis_vulgaris = 'Berberis vulgaris L.'
    Betula_alba = 'Betula alba (B. pendula / B. pubescens)'
    Betula_humilis = 'Betula humilis S'
    Betula_nana = 'Betula nana L.'
    Betula_pendula = 'Betula pendula Roth'
    Betula_pubescens = 'Betula pubescens Erh.'
    Buxus_sempervirens = 'Buxus sempervirens L.'
    Carpinus_betulus = 'Carpinus betulus L.'
    Castanea_sativa = 'Castanea sativa Gaertn.'
    Clematis_vitalba = 'Clematis vitalba L.'
    Cornus_mas = 'Cornus mas L.'
    Cornus_sanguinea = 'Cornus sanguinea L.'
    Corylus_avellana = 'Corylus avellana L.'
    Cotoneaster_integerrima = 'Cotoneaster integerrima Med.'
    Cotoneaster_tomentosa = 'Cotoneaster tomentosa Lindley'
    Crataegus_monogyna = 'Crataegus monogyna'
    Crataegus_oxyacantha = 'Crataegus oxyacantha'
    Cydonia_oblonga = 'Cydonia oblonga L.'
    Daphne_alpina = 'Daphne alpina L.'
    Daphne_cneorum = 'Daphne cneorum L.'
    Daphne_laureola = 'Daphne laureola L.'
    Daphne_mezereum = 'Daphne mezereum L.'
    Daphne_striata = 'Daphne striata Tratt.'
    Euonymus_europaeus = 'Euonymus europaeus L.'
    Euonymus_latifolius = 'Euonymus latifolius (L.) Mill.'
    Fagus_sylvatica = 'Fagus sylvatica L.'
    Frangula_alnus = 'Frangula alnus Mill.'
    Fraxinus_excelsior = 'Fraxinus excelsior L.'
    Hedera_helix = 'Hedera helix L.'
    Hippophae_rhamnoides = 'Hippophae rhamnoides L.'
    Ilex_aquifolium = 'Ilex aquifolium L.'
    Juglans_regia = 'Juglans regia L.'
    Juniperus_communis = 'Juniperus communis L.'
    Juniperus_nana = 'Juniperus nana Syme'
    Juniperus_sabina = 'Juniperus sabina L.'
    Laburnum_alpinum = 'Laburnum alpinum (Mill.) Prest.'
    Laburnum_anagyroides = 'Laburnum anagyroides Med.'
    Larix_decidua = 'Larix decidua Mill.'
    Ligustrum_vulgare = 'Ligustrum vulgare L.'
    Lonicera_alpigena = 'Lonicera alpigena L.'
    Lonicera_caprifolium = 'Lonicera caprifolium L.'
    Lonicera_coerulea = 'Lonicera coerulea L.'
    Lonicera_nigra = 'Lonicera nigra L.'
    Lonicera_periclymenum = 'Lonicera periclymenum L.'
    Lonicera_xylosteum = 'Lonicera xylosteum L.'
    Mespilus_germanica = 'Mespilus germanica L.'
    Ostrya_carpinifolia = 'Ostrya carpinifolia Scop.'
    Picea_abies = 'Picea abies Karsten'
    Pinus_Cembra = 'Pinus cembra L.'
    Pinus_Strobus = 'Pinus strobus L.'
    Pinus_mugo = 'Pinus mugo Turra'
    Pinus_nigra = 'Pinus nigra Arnold'
    Pinus_silvestris = 'Pinus silvestris L.'
    Pirus_communis = 'Pirus communis L.'
    Pirus_malus = 'Pirus malus L.'
    Platanus_orientalis = 'Platanus orientalis L. / P. occidentalis L.'
    Populus_alba = 'Populus alba L.'
    Populus_italica = 'Populus italica L.'
    Populus_nigra = 'Populus nigra L.'
    Populus_tremula = 'Populus tremula L.'
    Prunus_armeniaca = 'Prunus armeniaca L.'
    Prunus_avium = 'Prunus avium L.'
    Prunus_cerasifera = 'Prunus cerasifera Ehrh.'
    Prunus_cerasus = 'Prunus cerasus L.'
    Prunus_domestica = 'Prunus domestica L.'
    Prunus_insititia = 'Prunus insititia Julsen'
    Prunus_mahaleb = 'Prunus mahaleb L.'
    Prunus_padus = 'Prunus padus L.'
    Prunus_persica = 'Prunus persica (L.) Batsch'
    Prunus_spinosa = 'Prunus spinosa L.'
    Pseudotsuga_menziesii = 'Pseudotsuga menziesii (Mirb.) Franco'
    Quercus_petraea = 'Quercus petraea Liebl.'
    Quercus_pubescens = 'Quercus pubescens Willd.'
    Quercus_robur = 'Quercus robur L.'
    Rhamnus_cathartica = 'Rhamnus cathartica L.'
    Ribes_alpinum = 'Ribes alpinum L.'
    Ribes_nigrum = 'Ribes nigrum L.'
    Ribes_petraeum = 'Ribes petraeum Wulf.'
    Ribes_rubrum = 'Ribes rubrum L.'
    Ribes_uva_crispa = 'Ribes uva-crispa L.'
    Robinia_pseudoacacia = 'Robinia pseudoacacia L.'
    Rosa_arvensisn = 'Rosa arvensis Hudson'
    Rosa_canina = 'Rosa canina L.'
    Rosa_glauca = 'Rosa glauca Pourret'
    Rosa_pendulina = 'Rosa pendulina L.'
    Rosa_villosa = 'Rosa villosa L.'
    Salix_alba = 'Salix alba L.'
    Salix_appendiculata = 'Salix appendiculata Vill.'
    Salix_arbuscula = 'Salix arbuscula'
    Salix_aurita = 'Salix aurita L.'
    Salix_breviserrata = 'Salix breviserrata Flod.'
    Salix_caprea = 'Salix caprea L.'
    Salix_cinerea = 'Salix cinerea L.'
    Salix_daphnoides = 'Salix daphnoides Vill.'
    Salix_glabra = 'Salix glabra Scop.'
    Salix_glaucosericea = 'Salix glaucosericea Flod.'
    Salix_hastata = 'Salix hastata L.'
    Salix_helvetica = 'Salix helvetica Vill.'
    Salix_herbacea = 'Salix herbacea L.'
    Salix_incana = 'Salix incana'
    Salix_myrsinifolia = 'Salix myrsinifolia Salisb.'
    Salix_purpurea = 'Salix purpurea L.'
    Salix_repens = 'Salix repens L.'
    Salix_reticulata = 'Salix reticulata L.'
    Salix_retusa = 'Salix retusa L.'
    Salix_viminalis = 'Salix viminalis L.'
    Salix_waldsteiniana = 'Salix waldsteiniana Willd.'
    Sambucus_nigra = 'Sambucus nigra L.'
    Sambucus_racemosa = 'Sambucus racemosa L.'
    Sorbus_aria = 'Sorbus aria L.'
    Sorbus_aucuparia = 'Sorbus aucuparia L.'
    Sorbus_chamaemespilus = 'Sorbus chamaemespilus Crantz'
    Sorbus_domestica = 'Sorbus domestica L.'
    Sorbus_torminalis = 'Sorbus torminalis L.'
    Taxus_baccata = 'Taxus baccata L.'
    Tilia_cordata = 'Tilia cordata Mill.'
    Tilia_platyphyllos = 'Tilia platyphyllos Scop.'
    Ulmus_campestris = 'Ulmus campestris L.'
    Ulmus_laevis = 'Ulmus laevis Pallas'
    Ulmus_scabra = 'Ulmus scabra Mill.'
    Viburnum_lantana = 'Viburnum lantana L.'
    Viburnum_opulus = 'Viburnum opulus L.'
    Viscum_album = 'Viscum album L.'
    Vitis_vinifera = 'Vitis vinifera L.'


class DendroParameters(BaseModel):
    taxon: Optional[Taxon] = Field(None)
    image_scale_calibration: Optional[str] = Field(None, title='Image scale calibration', description='Smallest distance on scale card')
    image_processing_software: Optional[Set[str]] = Field(..., title='', description='Image processing software packages used')
    dendrochronology_dating_software: Optional[Set[str]] = Field(..., title='', description='Dendrochronology dating software packages used')

    class Config:
        title = "Measurement parameters"


class DendroResults(BaseModel):
    dating_youngest_ring: Optional[str] = Field(None, title='Date of the youngest ring')
    dating_last_ring: Optional[str] = Field(None, title='Date of the oldest ring')
    number_of_rings: Optional[int] = Field(None, title='Number of rings')
    comments: Optional[str] = Field(None, title='Comments', description='Comments with regards to generated research data')

    class Config:
        title = "Measurement results"


class Dendro(Measurement):
    document_type: str = Field("Dendrochronology", title='Document type', const=True) #OVERRIDE FROM DOCUMENT
    measurement_parameters: Optional[DendroParameters] = Field(None)
    measurement_results: Optional[DendroResults] = Field(None)
