from enum import Enum
from typing import Set, Optional

from pydantic import BaseModel, Field
from .measurement import Measurement


class Taxon(str, Enum):
    ABIES_ALBA = 'Abies alba Mill.'
    ACER_CAMPESTRE = 'Acer campestre L.'
    ACER_PLATANOIDES = 'Acer platanoides L.'
    ACER_PSEUDOPLATANUS = 'Acer pseudoplatanus L.'
    AESCULUS_HIPPOCASTANUM = 'Aesculus hippocastanum L.'
    ALNUS_GLUTINOSA = 'Alnus glutinosa Gaertn.'
    ALNUS_INCANA = 'Alnus incana DC.'
    ALNUS_VIRIDIS = 'Alnus viridis DC.'
    AMELANCHIER_OVALIS = 'Amelanchier ovalis Med.'
    BERBERIS_VULGARIS = 'Berberis vulgaris L.'
    BETULA_ALBA = 'Betula alba (B. pendula / B. pubescens)'
    BETULA_HUMILIS = 'Betula humilis S'
    BETULA_NANA = 'Betula nana L.'
    BETULA_PENDULA = 'Betula pendula Roth'
    BETULA_PUBESCENS = 'Betula pubescens Erh.'
    BUXUS_SEMPERVIRENS = 'Buxus sempervirens L.'
    CARPINUS_BETULUS = 'Carpinus betulus L.'
    CASTANEA_SATIVA = 'Castanea sativa Gaertn.'
    CLEMATIS_VITALBA = 'Clematis vitalba L.'
    CORNUS_MAS = 'Cornus mas L.'
    CORNUS_SANGUINEA = 'Cornus sanguinea L.'
    CORYLUS_AVELLANA = 'Corylus avellana L.'
    COTONEASTER_INTEGERRIMA = 'Cotoneaster integerrima Med.'
    COTONEASTER_TOMENTOSA = 'Cotoneaster tomentosa Lindley'
    CRATAEGUS_MONOGYNA = 'Crataegus monogyna'
    CRATAEGUS_OXYACANTHA = 'Crataegus oxyacantha'
    CYDONIA_OBLONGA = 'Cydonia oblonga L.'
    DAPHNE_ALPINA = 'Daphne alpina L.'
    DAPHNE_CNEORUM = 'Daphne cneorum L.'
    DAPHNE_LAUREOLA = 'Daphne laureola L.'
    DAPHNE_MEZEREUM = 'Daphne mezereum L.'
    DAPHNE_STRIATA = 'Daphne striata Tratt.'
    EUONYMUS_EUROPAEUS = 'Euonymus europaeus L.'
    EUONYMUS_LATIFOLIUS = 'Euonymus latifolius (L.) Mill.'
    FAGUS_SYLVATICA = 'Fagus sylvatica L.'
    FRANGULA_ALNUS = 'Frangula alnus Mill.'
    FRAXINUS_EXCELSIOR = 'Fraxinus excelsior L.'
    HEDERA_HELIX = 'Hedera helix L.'
    HIPPOPHAE_RHAMNOIDES = 'Hippophae rhamnoides L.'
    ILEX_AQUIFOLIUM = 'Ilex aquifolium L.'
    JUGLANS_REGIA = 'Juglans regia L.'
    JUNIPERUS_COMMUNIS = 'Juniperus communis L.'
    JUNIPERUS_NANA = 'Juniperus nana Syme'
    JUNIPERUS_SABINA = 'Juniperus sabina L.'
    LABURNUM_ALPINUM = 'Laburnum alpinum (Mill.) Prest.'
    LABURNUM_ANAGYROIDES = 'Laburnum anagyroides Med.'
    LARIX_DECIDUA = 'Larix decidua Mill.'
    LIGUSTRUM_VULGARE = 'Ligustrum vulgare L.'
    LONICERA_ALPIGENA = 'Lonicera alpigena L.'
    LONICERA_CAPRIFOLIUM = 'Lonicera caprifolium L.'
    LONICERA_COERULEA = 'Lonicera coerulea L.'
    LONICERA_NIGRA = 'Lonicera nigra L.'
    LONICERA_PERICLYMENUM = 'Lonicera periclymenum L.'
    LONICERA_XYLOSTEUM = 'Lonicera xylosteum L.'
    MESPILUS_GERMANICA = 'Mespilus germanica L.'
    OSTRYA_CARPINIFOLIA = 'Ostrya carpinifolia Scop.'
    PICEA_ABIES = 'Picea abies Karsten'
    PINUS_CEMBRA = 'Pinus cembra L.'
    PINUS_STROBUS = 'Pinus strobus L.'
    PINUS_MUGO = 'Pinus mugo Turra'
    PINUS_NIGRA = 'Pinus nigra Arnold'
    PINUS_SILVESTRIS = 'Pinus silvestris L.'
    PIRUS_COMMUNIS = 'Pirus communis L.'
    PIRUS_MALUS = 'Pirus malus L.'
    PLATANUS_ORIENTALIS = 'Platanus orientalis L. / P. occidentalis L.'
    POPULUS_ALBA = 'Populus alba L.'
    POPULUS_ITALICA = 'Populus italica L.'
    POPULUS_NIGRA = 'Populus nigra L.'
    POPULUS_TREMULA = 'Populus tremula L.'
    PRUNUS_ARMENIACA = 'Prunus armeniaca L.'
    PRUNUS_AVIUM = 'Prunus avium L.'
    PRUNUS_CERASIFERA = 'Prunus cerasifera Ehrh.'
    PRUNUS_CERASUS = 'Prunus cerasus L.'
    PRUNUS_DOMESTICA = 'Prunus domestica L.'
    PRUNUS_INSITITIA = 'Prunus insititia Julsen'
    PRUNUS_MAHALEB = 'Prunus mahaleb L.'
    PRUNUS_PADUS = 'Prunus padus L.'
    PRUNUS_PERSICA = 'Prunus persica (L.) Batsch'
    PRUNUS_SPINOSA = 'Prunus spinosa L.'
    PSEUDOTSUGA_MENZIESII = 'Pseudotsuga menziesii (Mirb.) Franco'
    QUERCUS_PETRAEA = 'Quercus petraea Liebl.'
    QUERCUS_PUBESCENS = 'Quercus pubescens Willd.'
    QUERCUS_ROBUR = 'Quercus robur L.'
    RHAMNUS_CATHARTICA = 'Rhamnus cathartica L.'
    RIBES_ALPINUM = 'Ribes alpinum L.'
    RIBES_NIGRUM = 'Ribes nigrum L.'
    RIBES_PETRAEUM = 'Ribes petraeum Wulf.'
    RIBES_RUBRUM = 'Ribes rubrum L.'
    RIBES_UVA_CRISPA = 'Ribes uva-crispa L.'
    ROBINIA_PSEUDOACACIA = 'Robinia pseudoacacia L.'
    ROSA_ARVENSISN = 'Rosa arvensis Hudson'
    ROSA_CANINA = 'Rosa canina L.'
    ROSA_GLAUCA = 'Rosa glauca Pourret'
    ROSA_PENDULINA = 'Rosa pendulina L.'
    ROSA_VILLOSA = 'Rosa villosa L.'
    SALIX_ALBA = 'Salix alba L.'
    SALIX_APPENDICULATA = 'Salix appendiculata Vill.'
    SALIX_ARBUSCULA = 'Salix arbuscula'
    SALIX_AURITA = 'Salix aurita L.'
    SALIX_BREVISERRATA = 'Salix breviserrata Flod.'
    SALIX_CAPREA = 'Salix caprea L.'
    SALIX_CINEREA = 'Salix cinerea L.'
    SALIX_DAPHNOIDES = 'Salix daphnoides Vill.'
    SALIX_GLABRA = 'Salix glabra Scop.'
    SALIX_GLAUCOSERICEA = 'Salix glaucosericea Flod.'
    SALIX_HASTATA = 'Salix hastata L.'
    SALIX_HELVETICA = 'Salix helvetica Vill.'
    SALIX_HERBACEA = 'Salix herbacea L.'
    SALIX_INCANA = 'Salix incana'
    SALIX_MYRSINIFOLIA = 'Salix myrsinifolia Salisb.'
    SALIX_PURPUREA = 'Salix purpurea L.'
    SALIX_REPENS = 'Salix repens L.'
    SALIX_RETICULATA = 'Salix reticulata L.'
    SALIX_RETUSA = 'Salix retusa L.'
    SALIX_VIMINALIS = 'Salix viminalis L.'
    SALIX_WALDSTEINIANA = 'Salix waldsteiniana Willd.'
    SAMBUCUS_NIGRA = 'Sambucus nigra L.'
    SAMBUCUS_RACEMOSA = 'Sambucus racemosa L.'
    SORBUS_ARIA = 'Sorbus aria L.'
    SORBUS_AUCUPARIA = 'Sorbus aucuparia L.'
    SORBUS_CHAMAEMESPILUS = 'Sorbus chamaemespilus Crantz'
    SORBUS_DOMESTICA = 'Sorbus domestica L.'
    SORBUS_TORMINALIS = 'Sorbus torminalis L.'
    TAXUS_BACCATA = 'Taxus baccata L.'
    TILIA_CORDATA = 'Tilia cordata Mill.'
    TILIA_PLATYPHYLLOS = 'Tilia platyphyllos Scop.'
    ULMUS_CAMPESTRIS = 'Ulmus campestris L.'
    ULMUS_LAEVIS = 'Ulmus laevis Pallas'
    ULMUS_SCABRA = 'Ulmus scabra Mill.'
    VIBURNUM_LANTANA = 'Viburnum lantana L.'
    VIBURNUM_OPULUS = 'Viburnum opulus L.'
    VISCUM_ALBUM = 'Viscum album L.'
    VITIS_VINIFERA = 'Vitis vinifera L.'


class DendroParameters(BaseModel):
    taxon: Optional[Taxon] = Field(None)
    image_scale_calibration: Optional[float] = Field(None, title='Image scale calibration', description='Smallest distance on scale card in mm')
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
    document_type: str = Field("dendro", const=True) #OVERRIDE FROM DOCUMENT
    measurement_parameters: Optional[DendroParameters] = Field(None)
    measurement_results: Optional[DendroResults] = Field(None)

    class Config:
        title = "Dendrochronology analysis"
