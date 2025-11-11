require 'csv'
require 'json'

module Jekyll
  class TypewritersDataGenerator < Generator
    safe true
    priority :low

    def generate(site)
      csv_path = File.join(site.source, 'content', 'typewriters.csv')
      json_path = File.join(site.source, '_data', 'typewriters.json')
      
      return unless File.exist?(csv_path)
      
      begin
        typewriters = []
        
        CSV.foreach(csv_path, headers: true) do |row|
          tw = {}
          row.to_h.each do |key, value|
            next if value.nil? || value.to_s.strip.empty? || value.to_s.downcase == 'nan'
            
            # Clean up the value
            cleaned = value.to_s.strip
            # Try to convert numbers
            if cleaned.match?(/^\d+\.0$/)
              cleaned = cleaned.to_i
            elsif cleaned.match?(/^\d+\.\d+$/)
              cleaned = cleaned.to_f
            elsif cleaned.match?(/^\d+$/)
              cleaned = cleaned.to_i
            end
            
            tw[key] = cleaned
          end
          
          # Only add if we have at least a brand or model
          if tw['Typewriter Brand'] || tw['Model']
            typewriters << tw
          end
        end
        
        # Ensure _data directory exists
        FileUtils.mkdir_p(File.dirname(json_path))
        
        # Write JSON file
        File.write(json_path, JSON.pretty_generate(typewriters))
        
        Jekyll.logger.info "Typewriters:", "Processed #{typewriters.length} typewriters from CSV"
      rescue => e
        Jekyll.logger.warn "Typewriters:", "Could not process typewriters.csv: #{e.message}"
      end
    end
  end
end

