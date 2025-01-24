export default function Footer() {
  return (
    <footer className="bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-wrap justify-between items-center">
          <div className="w-full md:w-auto text-center md:text-left mb-4 md:mb-0">
            <h3 className="text-lg font-medium mb-2">JML ORTHO</h3>
            <p className="text-sm text-gray-600">
              Профессиональная ортодонтическая клиника
            </p>
          </div>
          <div className="w-full md:w-auto text-center md:text-right">
            <p className="text-sm text-gray-600">
              © 2025 JML ORTHO. Все права защищены.
            </p>
            <p className="text-sm text-gray-600 mt-2">
              г. Москва, ул. Примерная, д. 1 | Тел: +7 (495) 123-45-67
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}

