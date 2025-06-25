## Purpose and Scope

This document describes the prompt template system used to guide Vision-Language Model (VLM) analysis in the crop detection system. Prompt templates define the structured JSON schema and analysis instructions that the VLM follows when processing agricultural images. These templates are central to generating consistent, comprehensive crop analysis results.

## Template Architecture

The prompt template system provides structured guidance to VLMs for agricultural image analysis. Templates are stored as text files and dynamically loaded during image processing.

**Template Integration Flow**: Templates are loaded from the assets directory and combined with encoded images to create VLM prompts that generate structured agricultural analysis.

## JSON Schema Structure

The prompt template defines a comprehensive JSON schema for agricultural analysis. The schema includes multiple hierarchical sections covering all aspects of crop and field assessment.

**Schema Hierarchy**: The JSON schema organizes agricultural analysis into logical sections from basic crop identification to advanced detection systems and recommendations.

## Detection Systems Integration

The template includes sophisticated detection capabilities for people, equipment, and animals in agricultural settings. These detection systems provide confidence scores and detailed categorization.

### Detection Schema Mapping

| Detection Type      | Key Fields                                              | Confidence Tracking     | Categorization                    |
|---------------------|---------------------------------------------------------|--------------------------|------------------------------------|
| People Detection    | `people_present`, `people_count`, `activities_observed` | `confidence_score (0–1)` | Activity-based classification     |
| Equipment Detection | `equipment_present`, `equipment_types`, `equipment_condition` | `confidence_score (0–1)` | Type and condition assessment     |
| Animal Detection    | `animals_present`, `animal_categories`, `animal_types_identified` | `confidence_score (0–1)` | Species and behavior categorization |

## Response Format Requirements

The template enforces strict JSON formatting requirements to ensure consistent VLM output parsing.

### Critical Formatting Rules

| Requirement        | Specification                              | Purpose                              |
|--------------------|---------------------------------------------|--------------------------------------|
| JSON Only          | Response must start with `{` and end with `}` | Parsing reliability                  |
| No Extra Text      | No additional text or explanations allowed | Clean data extraction                |
| Null Handling      | Use `null` for undeterminable fields        | Data integrity                       |
| Confidence Scores  | All confidence values between 0 and 1       | Standardized uncertainty measurement |

The template begins with explicit formatting instructions:

**CRITICAL: Your response must start with `{` and end with `}`. No other text allowed.**  

This ensures consistent parsing by downstream components in the system.