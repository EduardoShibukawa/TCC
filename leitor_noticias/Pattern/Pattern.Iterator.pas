unit Pattern.Iterator;

interface

type
  { Iterator }
  IIterator<T: Class> = interface
    procedure PrimeiroObjeto;
    procedure ProximoObjeto;
    function ObjetoAtual: T;
    function FimLista: boolean;
    function Buscar(const Indice: integer): T;
  end;

implementation

end.
