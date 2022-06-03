library(tibble)
library(gt)
library(dplyr)

general_quantity = tibble(
  tipo = c("Primaria", "Secundaria", "Terciaria", "Cuaternariaa"),
  experimentos = c(6096, 864, 1096),
  organoaminas = c(29, 6, 9)
)

cantidad_datos_por_solvente <- function(){
  general_quantity = tibble(
    solvente = c("GBL", "DMSO", "DMF"),
    experimentos = c(6096, 864, 1096),
    organoaminas = c(29, 6, 9)
  )
  general_quantity <- general_quantity %>% mutate(porcentaje = experimentos/sum(experimentos)*100)
  
  general_quantity %>%
    gt(rowname_col =  "solvente") %>% 
    #tab_header(
    # title = "                                                                                                                                                                                                                                                          por solvente", # Add a title
    #subtitle = "another useful subtitle" # And a subtitle
    #) %>% 
    cols_label(
      solvente = "Solvente",
      experimentos = "experimentos",
      organoaminas = "organoaminas",
      porcentaje = "%",
    ) %>%
    tab_stubhead(
      label = "Solvente" 
    ) %>%
    tab_spanner(
      label = "Cantidad de",
      columns = c(organoaminas, experimentos, porcentaje),
    ) %>%
    grand_summary_rows (
      columns = "experimentos",
      fns = list(Total =~sum(.)),
      formatter = fmt_number,
      decimals=0
    ) %>%
    grand_summary_rows (
      columns = "organoaminas",
      fns = list(Total =~sum(.)),
      formatter = fmt_number,
      decimals=0
    ) %>%
    tab_style(
      style = cell_text(weight = 'bold'),
      locations = list(cells_column_labels(),
                       cells_column_spanners(),
                       cells_stubhead()
      )
    ) %>%
    fmt_number(
      columns = porcentaje,
      decimals = 1
    ) %>%
    
    gtsave("cant_datos_por_amina_sv.pdf")
}
cantidad_datos_por_solvente()

features_plot <- function() {
  features = tibble(
    columnas = c("concentración de reactivos",
                 "    [orgánico]", "  [inorgánico]", "  [ácido]",
                 "solvente (GBL, DMSO o DMF)", "temperatura de reacción", "tiempos de agitación","organoamina ID", "propiedades FQ", "calidad de cristal"),
    cantidad = c(3, 1, 1, 1, 1, 1, 2, 1, 61, 1),
    tipo = c("Condiciones de Reacción (FEAT_RXN)", "Condiciones de Reacción (FEAT_RXN)", 
             "Condiciones de Reacción (FEAT_RXN)", "Condiciones de Reacción (FEAT_RXN)", 
             "Condiciones de Reacción (FEAT_RXN)", "Condiciones de Reacción (FEAT_RXN)", 
             "Condiciones de Reacción (FEAT_RXN)", "Condiciones de Reacción (FEAT_RXN)", 
             "Descriptor de Organoamina (FEAT_PHYCHEM)", "Etiqueta (LABEL)"),
  )
  features %>%
    gt(groupname_col = "tipo") %>%
    tab_style(
      style = list(cell_text(weight = 'bold', size = px(17))
      ),
      locations = cells_row_groups()
    ) %>%
    cols_label(
      columnas = "Tipo de Variables",
      cantidad = "Cantidad",
    ) %>%
    tab_options(
      column_labels.hidden = FALSE
    ) %>%
    tab_footnote(
      footnote = "E.g cantidad y tipo de: grupos funcionales, enlaces,
              donores/aceptores, etc",
      cells_body(columns = c(columnas),
                 rows= 9)
    ) %>%
    tab_style(
      style = cell_text(align = "left", indent = px(20)),
      locations = cells_body(columns = columnas, rows = c(2,3,4))
    ) %>%
    tab_style(
      style = cell_text(weight = "bold", size = px(20)),
      locations = cells_column_labels()
    ) %>%
    gtsave("../../figures/cantidad_tipo_features_con_nombres.pdf")
  
}
features_plot()

# Show the gt Table
tipo_aminas <- function(){
  df_amines_type <- read.csv(file = '../../data/metadata/type_amines_to_table.csv')
  feat_table <-gt(data=df_amines_type)
  feat_table %>%
    cols_label(
      tipo_amina = "tipo",
      index = "feature",
      count = "cantidad"
    )  %>%
    tab_header(
      title = "Tipo de Amina Presente",
      subtitle = "Cantidad de organoaminas según tipo de amina"
    ) %>%
    cols_align(
      align = "center",
      columns = count
    ) %>%
    gtsave("tipo_aminas_presentes.pdf", expand = 10)
}
tipo_var <- function(){
  df_var_type <- read.csv(file = '../../data/metadata/bin_ord_cont_table.csv')
  feat_table <-gt(data=df_var_type)
  feat_table %>%
    cols_label(
      type_var = "tipo de variable",
      propiedad = "cantidad"
    ) %>%
    cols_align(
      align = "center",
      columns = everything()
    ) #%>%
    #gtsave("tipo_aminas_presentes.pdf", expand = 10)
}


features_fq <- read.csv(file = '../../data/metadata/describe_feat_fq_description.csv')

feat_table <-gt(data=features_fq)

feat_table %>%
    cols_label(
    X25. = "25%",
    X50. = "50%",
    X75. = "75%"
  )  %>%
  gtsave("features_quimicas_description.pdf")

features_fq_by_type <- read.csv(file = '../../data/metadata/type_var_fq_bins.csv')

features_fq_by_type <-features_fq_by_type[, c('propiedad', 'count', 'type_var')]

features_fq_by_type_table %>%
  gt(data = features_fq_by_type,
     groupname_col = "type_var") %>%
    cols_label(
      propiedad = "Propiedad",
      count = "Valores Únicos",
      type_var = "Tipo de Variable"
    ) %>%
  tab_style(
    style = list(cell_text(weight = 'bold', size = px(18))
    ),
    locations = list(cells_row_groups(),
                     cells_column_labels()
                     )
  ) %>%
  tab_style(
    style = cell_borders(
      sides = c("top"),
      color = "white",
      weight = px(2)
    ),
    locations = list(cells_body()
    )
  ) %>%
  tab_options(row_group.as_column = TRUE) %>%
  tab_style(
    style = cell_borders(
      sides = c("top"),
      color = "black",
      weight = px(2)
    ),
    locations = list(cells_column_labels()
    )
  ) %>%
  tab_style(
    style = cell_borders(
      sides = c("right", "top", "bottom"),
      color = "black",
      weight = px(2)
    ),
    locations = list(cells_row_groups()
    )
  )%>%
  tab_style(
    style = cell_borders(
      sides = c("right", "left", "bottom"),
      color = NULL,
      weight = px(2)
    ),
    locations = list(cells_stubhead()
    )
  ) %>%
  tab_style(
    style = cell_borders(
      sides = c("top"),
      color = "black",
      weight = px(2)
    ),
    locations = list(cells_stubhead()
    )
  ) %>%
  tab_style(
    style = cell_borders(
      sides = c("bottom"),
      color = "black",
      weight = px(2)
    ),
    locations = cells_body(columns = c(propiedad, count), rows = c(57))
  ) 

features_fq_by_type_table %>%
  gt(data = features_fq_by_type,
     groupname_col = "type_var") %>%
  cols_label(
    propiedad = "Variable",
    count = "Valores Únicos",
    type_var = "Tipo de Variable"
  ) %>%
  tab_style(
    style = list(cell_text(weight = 'bold', size = px(18))
    ),
    locations = list(cells_row_groups(),
                     cells_column_labels()
    )
  ) %>%
  tab_style(
    style = cell_borders(
      sides = c("top"),
      color = "white",
      weight = px(2)
    ),
    locations = list(cells_body()
    )
  ) %>%
  tab_options(row_group.as_column = TRUE) %>%
  tab_style(
    style = cell_borders(
      sides = c("top"),
      color = "black",
      weight = px(2)
    ),
    locations = list(cells_column_labels()
    )
  ) %>%
  tab_style(
    style = cell_borders(
      sides = c("right", "top", "bottom"),
      color = NULL,
      weight = px(2)
    ),
    locations = list(cells_row_groups()
    )
  )%>%
  tab_style(
    style = cell_borders(
      sides = c("right", "left", "bottom"),
      color = NULL,
      weight = px(2)
    ),
    locations = list(cells_stubhead()
    )
  ) %>%
  tab_style(
    style = cell_borders(
      sides = c("top"),
      color = "black",
      weight = px(2)
    ),
    locations = list(cells_stubhead()
    )
  ) %>%
  tab_style(
    style = cell_borders(
      sides = c("bottom"),
      color = "black",
      weight = px(2)
    ),
    locations = list(cells_body(columns = c(propiedad, count), rows = c(57)),
                     cells_row_groups(groups = "continua")
    )
  ) %>%
  gtsave("feat_FQ_by_type_table.pdf")


  