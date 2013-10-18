Dir.glob('**/*').select { |fn| File.file?(fn) 
 begin
    text = File.read(fn)
    if fn  == "WebUI.py" || fn ==  "static/start.html"
        File.open(fn, "w") {|file| file.write(text.gsub(/www.congressbuddies.com/, "localhost:8080")) }
    end
  rescue

  end
}
