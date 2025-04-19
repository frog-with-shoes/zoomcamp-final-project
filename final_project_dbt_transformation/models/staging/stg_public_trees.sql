with source as (

    select
        *
    from {{ source('staging', 'tree-report-partitioned-clustered') }}
),

renamed as (

    select
        inv_type,
        emp_no,
        arrond,
        arrond_nom,
        rue,
        rue_cote,
        no_civique,
        emplacement,
        sigle,
        essence_latin,
        essence_fr,
        essence_ang,
        cast(dhp as string) as dhp,
        cast(date_releve as date) as date_releve,
        cast(date_plantation as date) as date_plantation,
        localisation,
        localisation_code,
        code_parc,
        nom_parc,
        rue_de,
        rue_a,
        distance_pave,
        distance_ligne_rue,
        stationnement_jour,
        stationnement_heure,
        district,
        arbre_remarquable,
        code_secteur,
        nom_secteur,
        coord_x,
        coord_y,
        longitude,
        latitude

    from source
    where essence_latin is not null 
)

select * from renamed
