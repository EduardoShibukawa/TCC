unit Pattern.Aggregate;

interface

uses
  Pattern.Iterator, System.Generics.Collections;

type
  { Aggregate }
  IAggregate<T: Class> = interface
    function GetLista: TObjectList<T>;
    function GetIterator: IIterator<T>;

  end;

implementation

end.
