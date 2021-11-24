# generated by datamodel-codegen:
#   filename:  dendro_dating_measurement.json
#   timestamp: 2021-11-03T21:37:55+00:00

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field
from .document import Document


class General(BaseModel):
    dossier_code: Optional[str] = Field(None, title='Dossier code')
    object_number: Optional[float] = Field(None, title='Object code')


class Sample(BaseModel):
    collection: str = Field(..., title='Collection')
    sample_code: str = Field(..., title='Sample Code')
    characteristics: Optional[str] = Field(None, title='Characteristics')
    material: Optional[str] = Field(None, title='Material')


class Taxon(str, Enum):
    Abies_alba_Mill_ = 'Abies alba Mill.'
    Acer_campestre_L_ = 'Acer campestre L.'
    Acer_platanoides_L_ = 'Acer platanoides L.'
    Acer_pseudoplatanus_L_ = 'Acer pseudoplatanus L.'
    Aesculus_hippocastanum_L_ = 'Aesculus hippocastanum L.'
    Alnus_glutinosa_Gaertn_ = 'Alnus glutinosa Gaertn.'
    Alnus_incana_DC_ = 'Alnus incana DC.'
    Alnus_viridis_DC_ = 'Alnus viridis DC.'
    Amelanchier_ovalis_Med_ = 'Amelanchier ovalis Med.'
    Berberis_vulgaris_L_ = 'Berberis vulgaris L.'
    Betula_alba__B__pendula___B__pubescens_ = 'Betula alba (B. pendula / B. pubescens)'
    Betula_humilis_S = 'Betula humilis S'
    Betula_nana_L_ = 'Betula nana L.'
    Betula_pendula_Roth = 'Betula pendula Roth'
    Betula_pubescens_Erh_ = 'Betula pubescens Erh.'
    Buxus_sempervirens_L_ = 'Buxus sempervirens L.'
    Carpinus_betulus_L_ = 'Carpinus betulus L.'
    Castanea_sativa_Gaertn_ = 'Castanea sativa Gaertn.'
    Clematis_vitalba_L_ = 'Clematis vitalba L.'
    Cornus_mas_L_ = 'Cornus mas L.'
    Cornus_sanguinea_L_ = 'Cornus sanguinea L.'
    Corylus_avellana_L_ = 'Corylus avellana L.'
    Cotoneaster_integerrima_Med_ = 'Cotoneaster integerrima Med.'
    Cotoneaster_tomentosa_Lindley = 'Cotoneaster tomentosa Lindley'
    Crataegus_monogyna = 'Crataegus monogyna'
    Crataegus_oxyacantha = 'Crataegus oxyacantha'
    Cydonia_oblonga_L_ = 'Cydonia oblonga L.'
    Daphne_alpina_L_ = 'Daphne alpina L.'
    Daphne_cneorum_L_ = 'Daphne cneorum L.'
    Daphne_laureola_L_ = 'Daphne laureola L.'
    Daphne_mezereum_L_ = 'Daphne mezereum L.'
    Daphne_striata_Tratt_ = 'Daphne striata Tratt.'
    Euonymus_europaeus_L_ = 'Euonymus europaeus L.'
    Euonymus_latifolius__L___Mill_ = 'Euonymus latifolius (L.) Mill.'
    Fagus_sylvatica_L_ = 'Fagus sylvatica L.'
    Frangula_alnus_Mill_ = 'Frangula alnus Mill.'
    Fraxinus_excelsior_L_ = 'Fraxinus excelsior L.'
    Hedera_helix_L_ = 'Hedera helix L.'
    Hippophae_rhamnoides_L_ = 'Hippophae rhamnoides L.'
    Ilex_aquifolium_L_ = 'Ilex aquifolium L.'
    Juglans_regia_L_ = 'Juglans regia L.'
    Juniperus_communis_L_ = 'Juniperus communis L.'
    Juniperus_nana_Syme = 'Juniperus nana Syme'
    Juniperus_sabina_L_ = 'Juniperus sabina L.'
    Laburnum_alpinum__Mill___Prest_ = 'Laburnum alpinum (Mill.) Prest.'
    Laburnum_anagyroides_Med_ = 'Laburnum anagyroides Med.'
    Larix_decidua_Mill_ = 'Larix decidua Mill.'
    Ligustrum_vulgare_L_ = 'Ligustrum vulgare L.'
    Lonicera_alpigena_L_ = 'Lonicera alpigena L.'
    Lonicera_caprifolium_L_ = 'Lonicera caprifolium L.'
    Lonicera_coerulea_L_ = 'Lonicera coerulea L.'
    Lonicera_nigra_L_ = 'Lonicera nigra L.'
    Lonicera_periclymenum_L_ = 'Lonicera periclymenum L.'
    Lonicera_xylosteum_L_ = 'Lonicera xylosteum L.'
    Mespilus_germanica_L_ = 'Mespilus germanica L.'
    Ostrya_carpinifolia_Scop_ = 'Ostrya carpinifolia Scop.'
    Picea_abies_Karsten = 'Picea abies Karsten'
    Pinus_Cembra_L_ = 'Pinus Cembra L.'
    Pinus_Strobus_L_ = 'Pinus Strobus L.'
    Pinus_mugo_Turra = 'Pinus mugo Turra'
    Pinus_nigra_Arnold = 'Pinus nigra Arnold'
    Pinus_silvestris_L_ = 'Pinus silvestris L.'
    Pirus_communis_L_ = 'Pirus communis L.'
    Pirus_malus_L_ = 'Pirus malus L.'
    Platanus_orientalis_L____P__occidentalis_L_ = (
        'Platanus orientalis L. / P. occidentalis L.'
    )
    Populus_alba_L_ = 'Populus alba L.'
    Populus_italica_L_ = 'Populus italica L.'
    Populus_nigra_L_ = 'Populus nigra L.'
    Populus_tremula_L_ = 'Populus tremula L.'
    Prunus_armeniaca_L_ = 'Prunus armeniaca L.'
    Prunus_avium_L_ = 'Prunus avium L.'
    Prunus_cerasifera_Ehrh_ = 'Prunus cerasifera Ehrh.'
    Prunus_cerasus_L_ = 'Prunus cerasus L.'
    Prunus_domestica_L_ = 'Prunus domestica L.'
    Prunus_insititia_Julsen = 'Prunus insititia Julsen'
    Prunus_mahaleb_L_ = 'Prunus mahaleb L.'
    Prunus_padus_L_ = 'Prunus padus L.'
    Prunus_persica__L___Batsch = 'Prunus persica (L.) Batsch'
    Prunus_spinosa_L_ = 'Prunus spinosa L.'
    Pseudotsuga_menziesii__Mirb___Franco = 'Pseudotsuga menziesii (Mirb.) Franco'
    Quercus_petraea_Liebl_ = 'Quercus petraea Liebl.'
    Quercus_pubescens_Willd_ = 'Quercus pubescens Willd.'
    Quercus_robur_L_ = 'Quercus robur L.'
    Rhamnus_cathartica_L_ = 'Rhamnus cathartica L.'
    Ribes_alpinum_L_ = 'Ribes alpinum L.'
    Ribes_nigrum_L_ = 'Ribes nigrum L.'
    Ribes_petraeum_Wulf_ = 'Ribes petraeum Wulf.'
    Ribes_rubrum_L_ = 'Ribes rubrum L.'
    Ribes_uva_crispa_L_ = 'Ribes uva-crispa L.'
    Robinia_pseudoacacia_L_ = 'Robinia pseudoacacia L.'
    Rosa_arvensis_Hudson = 'Rosa arvensis Hudson'
    Rosa_canina_L_ = 'Rosa canina L.'
    Rosa_glauca_Pourret = 'Rosa glauca Pourret'
    Rosa_pendulina_L_ = 'Rosa pendulina L.'
    Rosa_villosa_L_ = 'Rosa villosa L.'
    Salix_alba_L_ = 'Salix alba L.'
    Salix_appendiculata_Vill_ = 'Salix appendiculata Vill.'
    Salix_arbuscula = 'Salix arbuscula'
    Salix_aurita_L_ = 'Salix aurita L.'
    Salix_breviserrata_Flod_ = 'Salix breviserrata Flod.'
    Salix_caprea_L_ = 'Salix caprea L.'
    Salix_cinerea_L_ = 'Salix cinerea L.'
    Salix_daphnoides_Vill_ = 'Salix daphnoides Vill.'
    Salix_glabra_Scop_ = 'Salix glabra Scop.'
    Salix_glaucosericea_Flod_ = 'Salix glaucosericea Flod.'
    Salix_hastata_L_ = 'Salix hastata L.'
    Salix_helvetica_Vill_ = 'Salix helvetica Vill.'
    Salix_herbacea_L_ = 'Salix herbacea L.'
    Salix_incana = 'Salix incana'
    Salix_myrsinifolia_Salisb_ = 'Salix myrsinifolia Salisb.'
    Salix_purpurea_L_ = 'Salix purpurea L.'
    Salix_repens_L_ = 'Salix repens L.'
    Salix_reticulata_L_ = 'Salix reticulata L.'
    Salix_retusa_L_ = 'Salix retusa L.'
    Salix_viminalis_L_ = 'Salix viminalis L.'
    Salix_waldsteiniana_Willd_ = 'Salix waldsteiniana Willd.'
    Sambucus_nigra_L_ = 'Sambucus nigra L.'
    Sambucus_racemosa_L_ = 'Sambucus racemosa L.'
    Sorbus_aria_L_ = 'Sorbus aria L.'
    Sorbus_aucuparia_L_ = 'Sorbus aucuparia L.'
    Sorbus_chamaemespilus_Crantz = 'Sorbus chamaemespilus Crantz'
    Sorbus_domestica_L_ = 'Sorbus domestica L.'
    Sorbus_torminalis_L_ = 'Sorbus torminalis L.'
    Taxus_baccata_L_ = 'Taxus baccata L.'
    Tilia_cordata_Mill_ = 'Tilia cordata Mill.'
    Tilia_platyphyllos_Scop_ = 'Tilia platyphyllos Scop.'
    Ulmus_campestris_L_ = 'Ulmus campestris L.'
    Ulmus_laevis_Pallas = 'Ulmus laevis Pallas'
    Ulmus_scabra_Mill_ = 'Ulmus scabra Mill.'
    Viburnum_lantana_L_ = 'Viburnum lantana L.'
    Viburnum_opulus_L_ = 'Viburnum opulus L.'
    Viscum_album_L_ = 'Viscum album L.'
    Vitis_vinifera_L_ = 'Vitis vinifera L.'


class Software(str, Enum):
    Dendron_IV = 'Dendron IV'
    CooRecorder = 'CooRecorder'


class MeasurementParameters(BaseModel):
    measurement_technique: str = Field(..., title='Measurement technique')
    measurement_date: date = Field(..., title='Measurement date')
    measurement_index: str = Field(..., title='Measurement index')
    measurement_id: Optional[str] = Field(
        None,
        description='This is generated automatically from the previous two fields',
        title='Measurement Id',
    )
    taxon: Optional[Taxon] = Field(None, description='Taxonomy', title='Taxon')
    unit: Optional[str] = Field(None, title='Unit')
    software: Optional[Software] = Field(
        None, description='Datation software used', title='Software'
    )
    format: Optional[str] = Field(None, description='Data format', title='Format')


class Results(BaseModel):
    youngest_ring: Optional[str] = Field(None, title='Youngest ring')
    last_ring: Optional[str] = Field(None, title='Last ring')
    number_of_rings: Optional[float] = Field(
        None, description='Number of rings', title='Number of rings'
    )


class Dendro(Document):
    general: Optional[General] = Field(None, title='General')
    samples: Optional[List[Sample]] = Field(None, title='Samples')
    measurement_parameters: Optional[MeasurementParameters] = Field(None, title='Measurement parameters')
    results: Optional[Results] = Field(None, title='Results')
