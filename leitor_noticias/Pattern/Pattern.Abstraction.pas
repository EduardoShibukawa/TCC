unit Pattern.Abstraction;

interface

type
  { Abstraction }
  IExportador<T> = interface
    procedure ExportarDados(const Dados: TArray<T>);
  end;

implementation

end.
