-- Create table in default schema with enhanced description fields for text embeddings

CREATE TABLE crop_analysis_results
(
    -- Basic crop identification
    crop String,                                        -- Primary crop name
    alternate_names Array(String),                      -- Alternate/common names
    color Array(String),                                -- Dominant crop colors
    confidence Float32,                                 -- Model confidence (0 to 1)
    overall_description String,                         -- Comprehensive 2-3 sentence description of the image
    -- Growth stage
    growth_stage String,                                -- Crop stage: seedling/vegetative/etc.
    estimated_age_months Nullable(Float32),             -- Approximate crop age
    growth_description String,                          -- Detailed description of growth stage indicators
    -- Health assessment
    overall_health String,                              -- Health rating: excellent/good/fair/poor
    vigor_score Float32,                                -- Vigor score (0 to 1)
    disease_indicators Array(String),                   -- Detected diseases
    pest_indicators Array(String),                      -- Detected pest damage
    stress_indicators Array(String),                    -- Stress signs: drought/nutrient/etc.
    health_description String,                          -- Detailed plant health, leaf condition, and visible issues
    -- Field characteristics
    planting_pattern String,                            -- Row/scattered/etc.
    plant_density String,                               -- Low/medium/high
    field_size_estimate String,                         -- Field size category
    crop_uniformity String,                             -- Uniform/mixed/irregular
    weed_presence String,                               -- Weed level
    field_description String,                           -- Field layout, organization, spacing, and appearance
    -- Environmental context
    setting String,                                     -- Rural/urban/greenhouse/etc.
    terrain String,                                     -- Flat/sloped/etc.
    surrounding_vegetation String,                      -- Trees/other crops/buildings
    infrastructure_visible Array(String),               -- Irrigation/equipment/etc.
    weather_conditions String,                          -- Clear/cloudy/wet/dry
    environment_description String,                     -- Surrounding environment, landscape, and contextual elements
    -- Growing conditions
    moisture_level String,                              -- Soil moisture state
    soil_visibility String,                             -- Visibility of soil in image
    irrigation_evidence String,                         -- Sprinkler/drip/furrow/etc.
    season_indication String,                           -- Growing/dormant/harvest_time
    conditions_description String,                      -- Soil conditions, moisture indicators, and seasonal factors
    -- Agricultural insights
    farming_type String,                                -- Commercial/subsistence/experimental
    management_quality String,                          -- Farm management quality
    harvest_readiness String,                           -- Crop readiness for harvest
    estimated_months_to_harvest Nullable(Float32),      -- Remaining time to harvest
    management_description String,                      -- Farming practices, management quality, and cultivation methods
    -- Recommendations
    recommendations Array(String),                      -- Suggested farming actions
    recommendations_summary String,                     -- Consolidated summary of key recommendations and priority actions
    -- Semantic search fields
    semantic_tags Array(String),                        -- Relevant agricultural keywords for tagging
    search_context String,                              -- Natural language summary for search indexing
    -- Image metadata
    image_quality String,                               -- Image quality rating
    lighting_conditions String,                         -- Natural/artificial/low light
    viewing_angle String,                               -- Aerial/ground/close-up
    coverage_area String,                               -- Single plant / field overview
    visual_description String,                          -- Image quality, perspective, and visible areas
    -- Embedding vectors (for hybrid approach)
    text_embedding Array(Float32),                      -- Text embedding from descriptions
    image_embedding Array(Float32),                     -- Image embedding from visual features
    hybrid_embedding Array(Float32),                    -- Combined text + image embedding
    -- Timestamps and metadata
    image_path String,                                  -- Path to original image file
    startDateTime DateTime,                             -- Analysis start time
    endDateTime DateTime,                               -- Analysis end time
    duration Float32                                     -- Duration in seconds (end - start)
)
ENGINE = MergeTree
ORDER BY (crop, startDateTime)
SETTINGS index_granularity = 8192;

-- Create indexes for better query performance
ALTER TABLE crop_analysis_results ADD INDEX idx_crop_health (crop, overall_health) TYPE bloom_filter GRANULARITY 1;
ALTER TABLE crop_analysis_results ADD INDEX idx_growth_stage (growth_stage) TYPE bloom_filter GRANULARITY 1;
ALTER TABLE crop_analysis_results ADD INDEX idx_semantic_tags (semantic_tags) TYPE bloom_filter GRANULARITY 1;

-- Example of how to insert data with the new schema
-- INSERT INTO crop_analysis_results VALUES (
--     'Tomato',                                          -- crop
--     ['Lycopersicon esculentum', 'Solanum lycopersicum'], -- alternate_names
--     ['green', 'yellow'],                               -- color
--     0.9,                                              -- confidence
--     'Large commercial tomato field showing plants in fruiting stage with visible green tomatoes and some yellowing leaves indicating possible drought stress.', -- overall_description
--     'fruiting',                                       -- growth_stage
--     3,                                                -- estimated_age_months
--     'Tomato plants are in the fruiting stage with small green tomatoes visible on the vines, indicating active fruit development.', -- growth_description
--     'good',                                           -- overall_health
--     0.8,                                              -- vigor_score
--     ['yellowing leaves'],                             -- disease_indicators
--     [],                                               -- pest_indicators
--     ['drought'],                                      -- stress_indicators
--     'Plants show generally good health with strong green foliage, though some lower leaves display yellowing which may indicate water stress or natural senescence.', -- health_description
--     'rows',                                           -- planting_pattern
--     'medium',                                         -- plant_density
--     'large_commercial',                               -- field_size_estimate
--     'uniform',                                        -- crop_uniformity
--     'none',                                           -- weed_presence
--     'Well-organized commercial field with plants arranged in neat rows with consistent spacing, indicating professional farming practices.', -- field_description
--     'rural',                                          -- setting
--     'flat',                                           -- terrain
--     'trees',                                          -- surrounding_vegetation
--     ['irrigation'],                                   -- infrastructure_visible
--     'dry',                                            -- weather_conditions
--     'Rural agricultural setting on flat terrain with trees visible in the background and clear evidence of irrigation infrastructure.', -- environment_description
--     'dry',                                            -- moisture_level
--     'partially_visible',                              -- soil_visibility
--     'drip',                                           -- irrigation_evidence
--     'growing_season',                                 -- season_indication
--     'Soil appears dry with visible drip irrigation lines, indicating controlled water management during active growing season.', -- conditions_description
--     'commercial',                                     -- farming_type
--     'good',                                           -- management_quality
--     'not_ready',                                      -- harvest_readiness
--     2,                                                -- estimated_months_to_harvest
--     'Professional commercial operation with evidence of good management practices including proper spacing, irrigation, and crop maintenance.', -- management_description
--     ['Implement regular irrigation to prevent drought stress', 'Monitor for disease and pests', 'Test soil and apply fertilizers'], -- recommendations
--     'Priority actions include increasing irrigation frequency to address drought stress and implementing regular monitoring for optimal crop health.', -- recommendations_summary
--     ['tomato', 'commercial farming', 'fruiting stage', 'drought stress', 'irrigation'], -- semantic_tags
--     'Commercial tomato field in fruiting stage showing good management with drip irrigation but experiencing drought stress requiring increased watering.', -- search_context
--     'good',                                           -- image_quality
--     'natural_daylight',                               -- lighting_conditions
--     'ground_level',                                   -- viewing_angle
--     'field_overview',                                 -- coverage_area
--     'Clear daylight image taken at ground level providing good overview of the tomato field with adequate detail for analysis.', -- visual_description
--     [],                                               -- text_embedding (populated by embedding pipeline)
--     [],                                               -- image_embedding (populated by embedding pipeline)
--     [],                                               -- hybrid_embedding (populated by embedding pipeline)
--     '/path/to/image.jpg',                             -- image_path
--     '2025-06-08 19:05:19',                            -- startDateTime
--     '2025-06-08 19:09:10',                            -- endDateTime
--     230.91                                            -- duration
-- );