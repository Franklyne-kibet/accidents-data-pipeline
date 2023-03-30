{# This macro returns the description of accidents severity #}

{% macro get_accident_severity(severity) -%}

    case {{ severity }}
        when 1 then 'low impact'
        when 2 then 'moderate impact'
        when 3 then 'high impact'
        when 4 then 'critical impact'
    end

{%- endmacro %}